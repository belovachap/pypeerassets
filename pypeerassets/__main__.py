'''Contains main protocol logic like assembly of proof-of-timeline and parsing
deck info.
'''

from binascii import unhexlify
import concurrent.futures
from decimal import Decimal, getcontext
from typing import Generator, Union

from pypeerassets.exceptions import *
from pypeerassets.kutil import Kutil
from pypeerassets.networks import NETWORKS
from pypeerassets.pa_constants import params, param_query
from pypeerassets.pautils import (
    deck_issue_mode,
    find_deck_spawns,
    find_tx_sender,
    issue_mode_to_enum,
    load_deck_p2th_into_local_node,
    parse_card_transfer_metainfo,
    parse_deckspawn_metainfo,
    postprocess_card,
    read_tx_opreturn,
    tx_serialization_order,
    validate_card_transfer_p2th,
    validate_deckspawn_p2th,
)
from pypeerassets.protocol import *
from pypeerassets.provider import Provider, RpcNode
from pypeerassets.transactions import (
    MutableTransaction,
    Transaction,
    TxOut,
    calculate_tx_fee,
    find_parent_outputs,
    make_raw_transaction,
    nulldata_script,
    p2pkh_script,
    tx_output,
)


getcontext().prec = 6


def deck_parser(args: Union[Provider, dict, int, str], prod: bool=True) -> Deck:
    '''deck parser function'''

    provider = args[0]
    raw_tx = args[1]
    deck_version = args[2]
    p2th = args[3]

    try:
        validate_deckspawn_p2th(provider, raw_tx, p2th)

        d = parse_deckspawn_metainfo(read_tx_opreturn(raw_tx), deck_version)

        if d:

            d["id"] = raw_tx["txid"]
            try:
                d["time"] = raw_tx["blocktime"]
            except KeyError:
                d["time"] = 0
            d["issuer"] = find_tx_sender(provider, raw_tx)
            d["network"] = provider.network
            d["production"] = prod
            return Deck(**d)

    except (InvalidDeckSpawn, InvalidDeckMetainfo, InvalidDeckVersion, InvalidNulldataOutput) as err:
        pass


def find_all_valid_decks(provider: Provider, deck_version: int, prod: bool=True) -> Generator:
    '''
    Scan the blockchain for PeerAssets decks, returns list of deck objects.
    : provider - provider instance
    : version - deck protocol version (0, 1, 2, ...)
    : test True/False - test or production P2TH
    '''

    pa_params = param_query(provider.network)

    if prod:
        p2th = pa_params.P2TH_addr
    else:
        p2th = pa_params.test_P2TH_addr

    if isinstance(provider, RpcNode):
        deck_spawns = (provider.getrawtransaction(i, 1) for i in find_deck_spawns(provider))

    else:
        try:
            deck_spawns = (provider.getrawtransaction(i, 1) for i in
                           provider.listtransactions(p2th))
        except TypeError as err:  # it will except if no transactions are found on this P2TH
            raise EmptyP2THDirectory(err)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as th:
        for result in th.map(deck_parser, ((provider, rawtx, deck_version, p2th) for rawtx in deck_spawns)):
            if result:
                yield result


def sign_transaction(provider: Provider, mutable_tx: MutableTransaction,
                     key: Kutil) -> Transaction:
    '''sign mutable transaction with Kutil'''

    parent_output = find_parent_outputs(provider, mutable_tx.ins[0])
    return key.sign_transaction(parent_output, mutable_tx)


def _increase_fee_and_sign(provider: Provider, key: Kutil, change_sum: Decimal,
                           inputs: dict, txouts: list):
    '''when minimal fee wont cut it'''

    # change output is last of transaction outputs
    txouts[-1] = tx_output(value=change_sum, n=txouts[-1].n, script=txouts[-1].script_pubkey)

    mutable_tx = make_raw_transaction(inputs['utxos'], txouts)
    signed = sign_transaction(provider, mutable_tx, key)

    return signed


def find_deck(provider: Provider, key: str, version: int, prod=True) -> list:
    '''Find specific deck by deck id.'''

    pa_params = param_query(provider.network)
    if prod:
        p2th = pa_params.P2TH_addr
    else:
        p2th = pa_params.test_P2TH_addr

    rawtx = provider.getrawtransaction(key, 1)
    deck = deck_parser((provider, rawtx, 1, p2th))

    return deck


def deck_spawn(provider: Provider, key: Kutil, deck: Deck, inputs: dict, change_address: str) -> str:
    '''Creates Deck spawn raw transaction.
       : key - Kutil object which we'll use to sign the tx
       : deck - Deck object
       : card - CardTransfer object
       : inputs - utxos (has to be owned by deck issuer)
       : change_address - address to send the change to
    '''

    network = NETWORKS[deck.network]()
    pa_params = param_query(deck.network)

    if deck.production:
        p2th_addr = pa_params.P2TH_addr
    else:
        p2th_addr = pa_params.test_P2TH_addr

    #  first round of txn making is done by presuming minimal fee
    change_sum = Decimal(inputs['total'] - network.min_tx_fee - pa_params.P2TH_fee)

    txouts = [
        tx_output(value=pa_params.P2TH_fee, n=0, script=p2pkh_script(p2th_addr)),  # p2th
        tx_output(value=0, n=1, script=nulldata_script(deck.metainfo_to_protobuf)),  # op_return
        tx_output(value=change_sum, n=2, script=p2pkh_script(change_address))  # change
              ]

    mutable_tx = make_raw_transaction(inputs['utxos'], txouts)
    signed = sign_transaction(provider, mutable_tx, key)

    fee = Decimal(calculate_tx_fee(signed.size))

    # if 0.01 ppc fee is enough to cover the tx size
    if Decimal(network.min_tx_fee) == fee:
        return signed.hexlify()

    change_sum = Decimal(inputs['total'] - fee - pa_params.P2TH_fee)

    signed = _increase_fee_and_sign(provider, key, change_sum, inputs, txouts)
    return signed.hexlify()


def deck_transfer(provider: Provider, key: Kutil, deck: Deck,
                  inputs: list, change_address: str):
    '''
    The deck transfer transaction is a special case of the deck spawn transaction.
    Instead of registering a new asset, the deck transfer transaction transfers ownership from vin[1] to vin[0],
    meaning that both parties are required to sign the transfer transaction for it to be accepted in the blockchain.
    '''
    raise NotImplementedError


def find_card_transfers(provider: Provider, deck: Deck) -> Generator:
    '''find all <deck> card transfers'''

    card_transfers = []

    if isinstance(provider, RpcNode):
        batch_data = [('getrawtransaction', [i["txid"], 1] ) for i in provider.listtransactions(deck.id)]
        result = provider.batch(batch_data)
        if result is not None:
            card_transfers = [i['result'] for i in result if result ]  
    else:
        try:
            card_transfers = (provider.getrawtransaction(i, 1) for i in
                              provider.listtransactions(deck.p2th_address))
        except TypeError:
            raise EmptyP2THDirectory({'error': 'No cards found on this deck.'})

    def card_parser(args) -> list:
        '''this function wraps all the card transfer parsing'''

        provider = args[0]
        deck = args[1]
        raw_tx = args[2]
        cards = []

        try:
            validate_card_transfer_p2th(deck, raw_tx)  # validate P2TH first
            card_metainfo = parse_card_transfer_metainfo(read_tx_opreturn(raw_tx), deck.version)
            vouts = raw_tx["vout"]
            sender = find_tx_sender(provider, raw_tx)

            try:  # try to get block seq number
                blockseq = tx_serialization_order(provider, raw_tx["blockhash"], raw_tx["txid"])
            except KeyError:
                blockseq = None
            try:  # try to get block number of block when this tx was written
                blocknum = provider.getblock(raw_tx["blockhash"])["height"]
            except KeyError:
                blocknum = None

            cards = postprocess_card(card_metainfo, raw_tx, sender,
                                     vouts, blockseq, blocknum, deck)
            cards = [CardTransfer(**card) for card in cards]

        except (InvalidCardTransferP2TH, CardVersionMistmatch, CardNumberOfDecimalsMismatch) as e:
            return False

        return cards

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as th:
        for result in th.map(card_parser, ((provider, deck, i) for i in card_transfers)):
            if result:
                yield result


def card_issue(provider: Provider, key: Kutil, deck: Deck,
               card: CardTransfer, inputs: dict,
               change_address: str) -> str:
    '''Create card issue transaction.
       : key - Kutil object which we'll use to sign the tx
       : deck - Deck object
       : card - CardTransfer object
       : inputs - utxos (has to be owned by deck issuer)
       : change_address - address to send the change to
    '''

    network = NETWORKS[deck.network]()
    pa_params = param_query(deck.network)

    txouts = [
        tx_output(value=pa_params.P2TH_fee, n=0, script=p2pkh_script(deck.p2th_address)),  # deck p2th
        tx_output(value=0, n=1, script=nulldata_script(card.metainfo_to_protobuf))  # op_return
    ]

    for addr, index in zip(card.receiver, range(len(card.receiver))):
        txouts.append(   # TxOut for each receiver, index + 2 because we have two outs already
            tx_output(value=0, n=index+2, script=p2pkh_script(addr))
        )

    #  first round of txn making is done by presuming minimal fee
    change_sum = Decimal(inputs['total'] - network.min_tx_fee - pa_params.P2TH_fee)

    txouts.append(
        tx_output(value=change_sum, n=len(txouts)+1, script=p2pkh_script(change_address))
        )

    mutable_tx = make_raw_transaction(inputs['utxos'], txouts)
    signed = sign_transaction(provider, mutable_tx, key)

    fee = Decimal(calculate_tx_fee(signed.size))

    # if 0.01 ppc fee is enough to cover the tx size
    if Decimal(network.min_tx_fee) == calculate_tx_fee(signed.size):
        return signed.hexlify()

    change_sum = Decimal(inputs['total'] - fee - pa_params.P2TH_fee)

    signed = _increase_fee_and_sign(provider, key, change_sum, inputs, txouts)
    return signed.hexlify()


def card_burn(provider: Provider, key: Kutil, deck: Deck,
              card: CardTransfer, inputs: list,
              change_address: str) -> str:
    '''Create card burn transaction, cards are burned by sending the cards back to deck issuer.
       : key - Kutil object which we'll use to sign the tx
       : deck - Deck object
       : card - CardTransfer object
       : inputs - utxos (has to be owned by deck issuer)
       : change_address - address to send the change to
       '''

    assert deck.issuer == card.receiver[0], {"error": "First recipient must be deck issuer."}

    network = NETWORKS[deck.network]()
    pa_params = param_query(deck.network)

    txouts = [
        tx_output(value=pa_params.P2TH_fee, n=0, script=p2pkh_script(deck.p2th_address)),  # deck p2th
        tx_output(value=0, n=1, script=nulldata_script(card.metainfo_to_protobuf)),  # op_return
        tx_output(value=0, n=2, script=p2pkh_script(card.receiver[0]))  # p2pkh receiver[0]
    ]

    #  first round of txn making is done by presuming minimal fee
    change_sum = Decimal(inputs['total'] - network.min_tx_fee - pa_params.P2TH_fee)

    txouts.append(
        tx_output(value=change_sum, n=len(outputs)+1, script=p2pkh_script(change_address))
        )

    mutable_tx = make_raw_transaction(inputs['utxos'], txouts)
    signed = sign_transaction(provider, mutable_tx, key)

    # if 0.01 ppc fee is enough to cover the tx size
    if network.min_tx_fee == calculate_tx_fee(signed.size):
        return signed.hexlify()

    fee = Decimal(calculate_tx_fee(signed.size))

    if Decimal(network.min_tx_fee) == fee:
        return signed.hexlify()

    change_sum = Decimal(inputs['total'] - fee - pa_params.P2TH_fee)

    signed = _increase_fee_and_sign(provider, key, change_sum, inputs, txouts)
    return signed.hexlify()


def card_transfer(deck: Deck, card: CardTransfer, inputs: list, change_address: str) -> str:
    '''Standard peer-to-peer card transfer.
       : deck - Deck object
       : card - CardTransfer object
       : inputs - utxos (has to be owned by deck issuer)
       : change_address - address to send the change to
       '''

    network = NETWORKS[deck.network]()
    pa_params = param_query(deck.network)

    outputs = [
        tx_output(value=pa_params.P2TH_fee, n=0, script=p2pkh_script(deck.p2th_address)),  # deck p2th
        tx_output(value=0, n=1, script=nulldata_script(card.metainfo_to_protobuf))  # op_return
    ]

    for addr, index in zip(card.receiver, range(len(card.receiver))):
        outputs.append(   # TxOut for each receiver, index + 2 because we have two outs already
            tx_output(value=0, n=index+2, script=p2pkh_script(addr))
        )

    #  first round of txn making is done by presuming minimal fee
    change_sum = Decimal(inputs['total'] - network.min_tx_fee - pa_params.P2TH_fee)

    outputs.append(
        tx_output(value=change_sum, n=len(outputs)+1, script=p2pkh_script(change_address))
        )

    mutable_tx = make_raw_transaction(inputs['utxos'], txouts)
    signed = sign_transaction(provider, mutable_tx, key)

    # if 0.01 ppc fee is enough to cover the tx size
    if network.min_tx_fee == calculate_tx_fee(signed.size):
        return signed.hexlify()

    fee = Decimal(calculate_tx_fee(signed.size))

    if Decimal(network.min_tx_fee) == fee:
        return signed.hexlify()

    change_sum = Decimal(inputs['total'] - fee - pa_params.P2TH_fee)

    signed = _increase_fee_and_sign(provider, key, change_sum, inputs, txouts)
    return signed.hexlify()
