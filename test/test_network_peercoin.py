from decimal import Decimal

from pypeerassets.network.peercoin import Peercoin


def test_network_parameters():
    "Check that the network parameters are set properly."
    peercoin = Peercoin()
    assert peercoin.name == "peercoin"
    assert peercoin.short_name == "ppc"
    assert peercoin.pub_key_hash == b'37'
    assert peercoin.wif_prefix == b'b7'
    assert peercoin.script_hash == b'75'
    assert peercoin.magic_bytes == b'e6e8e9e5'
    assert peercoin.msg_prefix == b'\x17PPCoin Signed Message:\n'
    assert peercoin.min_tx_fee == Decimal(0.01)
    assert peercoin.min_vout_value == 0
    assert peercoin.tx_timestamp == True
    assert peercoin.denomination == Decimal('1e6')
    assert peercoin.is_testnet == False
