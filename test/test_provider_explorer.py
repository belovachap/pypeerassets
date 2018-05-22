from decimal import Decimal

from pypeerassets.networks import NETWORKS
from pypeerassets.provider.explorer import Explorer


def test_explorer_is_testnet():

    explorer = Explorer(NETWORKS["peercoin"]())

    assert isinstance(explorer.network.is_testnet, bool)
    assert explorer.network.is_testnet is False


def test_explorer_network():

    assert Explorer(NETWORKS["peercoin"]()).network.name == "peercoin"


def test_explorer_getblockcount():

    assert isinstance(Explorer(NETWORKS["peercoin"]()).getblockcount(), int)


def test_explorer_getblock():

    provider = Explorer(NETWORKS["peercoin"]())
    assert isinstance(provider.getblock('00000000000da9a26b4f4ce3f1f286438ec2198e5f60d108fafa700061b486e7'), dict)


def test_explorer_get_block_hash():

    assert isinstance(Explorer(NETWORKS["peercoin"]()).getblockhash(3378), str)


def test_explorer_getdifficulty():

    assert isinstance(Explorer(NETWORKS["peercoin"]()).getdifficulty(), dict)


def test_explorer_getbalance():

    assert isinstance(Explorer(NETWORKS["peercoin"]()).getbalance(
                      'PHvDhfz1dGyPbZZ3Qnp56y92zmy98sncZT'), Decimal)


def test_explorer_getreceivedbyaddress():

    assert isinstance(Explorer(NETWORKS["peercoin"]()).getreceivedbyaddress(
                      'PHvDhfz1dGyPbZZ3Qnp56y92zmy98sncZT'), Decimal)


def test_explorer_listunspent():

    assert isinstance(Explorer(NETWORKS["peercoin"]()).listunspent(
                      'PAdonateFczhZuKLkKHozrcyMJW7Y6TKvw'), list)


def test_explorer_getrawtransaction():

    assert isinstance(Explorer(NETWORKS["peercoin"]()).getrawtransaction(
                      '34d19bf5a5c757d5bcbf83a91ad9bc04365c58a035a6bf728bce8013ad04c173'), dict)


def test_explorer_listtransactions():

    assert isinstance(Explorer(NETWORKS["peercoin"]()).listtransactions(
                      'PHvDhfz1dGyPbZZ3Qnp56y92zmy98sncZT'), list)
