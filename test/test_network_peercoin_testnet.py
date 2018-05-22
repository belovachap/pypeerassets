from decimal import Decimal

from pypeerassets.network.peercoin_testnet import PeercoinTestnet


def test_network_parameters():
    "Check that the network parameters are set properly."
    peercoin_testnet = PeercoinTestnet()
    assert peercoin_testnet.name == "peercoin-testnet"
    assert peercoin_testnet.short_name == "tppc"
    assert peercoin_testnet.pub_key_hash == b'6f'
    assert peercoin_testnet.wif_prefix == b'ef'
    assert peercoin_testnet.script_hash == b'c4'
    assert peercoin_testnet.magic_bytes == b'cbf2c0ef'
    assert peercoin_testnet.msg_prefix == b'\x17PPCoin Signed Message:\n'
    assert peercoin_testnet.min_tx_fee == Decimal(0.01)
    assert peercoin_testnet.min_vout_value == 0
    assert peercoin_testnet.tx_timestamp == True
    assert peercoin_testnet.denomination == Decimal('1e6')
    assert peercoin_testnet.is_testnet == True
