from decimal import Decimal

from pypeerassets.networks import NETWORKS
from pypeerassets.provider.cryptoid import Cryptoid


def test_cryptoid_is_testnet():

    cryptoid = Cryptoid(NETWORKS["peercoin"]())

    assert isinstance(cryptoid.network.is_testnet, bool)
    assert cryptoid.network.is_testnet is False


def test_crypotid_network():

    assert Cryptoid(NETWORKS["peercoin"]()).network.name == "peercoin"


def test_cryptoid_getblockcount():

    assert isinstance(Cryptoid(NETWORKS["peercoin"]()).getblockcount(), int)


def test_cryptoid_getblock():

    provider = Cryptoid(NETWORKS["peercoin-testnet"]())
    assert isinstance(provider.getblock('0000000429a1e623da44a7430b9d9ae377bc2da203043c444c313b2d4390eba2'), dict)


def test_cryptoid_get_block_hash():

    assert isinstance(Cryptoid(NETWORKS["peercoin"]()).getblockhash(3378), str)


def test_cryptoid_getdifficulty():

    assert isinstance(Cryptoid(NETWORKS["peercoin"]()).getdifficulty(), float)


def test_cryptoid_getbalance():

    assert isinstance(Cryptoid(NETWORKS["peercoin"]()).getbalance(
                      'PHvDhfz1dGyPbZZ3Qnp56y92zmy98sncZT'), Decimal)


def test_cryptoid_getreceivedbyaddress():

    assert isinstance(Cryptoid(NETWORKS["peercoin"]()).getreceivedbyaddress(
                      'PHvDhfz1dGyPbZZ3Qnp56y92zmy98sncZT'), Decimal)


def test_cryptoid_listunspent():

    assert isinstance(Cryptoid(NETWORKS["peercoin"]()).listunspent(
                      'PAdonateFczhZuKLkKHozrcyMJW7Y6TKvw'), list)


def test_cryptoid_getrawtransaction():

    assert isinstance(Cryptoid(NETWORKS["peercoin"]()).getrawtransaction(
                      '34d19bf5a5c757d5bcbf83a91ad9bc04365c58a035a6bf728bce8013ad04c173'), dict)


def test_cryptoid_listtransactions():

    assert isinstance(Cryptoid(NETWORKS["peercoin-testnet"]()).listtransactions(
                      'msPLoMcHpn6Y28pPKwATG411m5X7Vodu3m'), list)
