from decimal import Decimal

from pypeerassets.network.bitcoin_testnet import BitcoinTestnet


def test_network_parameters():
    "Check that the network parameters are set properly."
    bitcoin_testnet = BitcoinTestnet()
    assert bitcoin_testnet.name == "bitcoin-testnet"
    assert bitcoin_testnet.short_name == "tbtc"
    assert bitcoin_testnet.pub_key_hash == b'6f'
    assert bitcoin_testnet.wif_prefix == b'ef'
    assert bitcoin_testnet.script_hash == b'c4'
    assert bitcoin_testnet.magic_bytes == b'dab5bffa'
    assert bitcoin_testnet.msg_prefix == b'\x18Bitcoin Signed Message:\n'
    assert bitcoin_testnet.min_tx_fee == 0
    assert bitcoin_testnet.min_vout_value == 0
    assert bitcoin_testnet.tx_timestamp == False
    assert bitcoin_testnet.denomination == Decimal('1e8')
    assert bitcoin_testnet.is_testnet == True
