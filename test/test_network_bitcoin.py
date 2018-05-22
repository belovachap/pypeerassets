from decimal import Decimal

from pypeerassets.network.bitcoin import Bitcoin


def test_network_parameters():
    "Check that the network parameters are set properly."
    bitcoin = Bitcoin()
    assert bitcoin.name == "bitcoin"
    assert bitcoin.short_name == "btc"
    assert bitcoin.pub_key_hash == b'00'
    assert bitcoin.wif_prefix == b'80'
    assert bitcoin.script_hash == b'05'
    assert bitcoin.magic_bytes == b'd9b4bef9'
    assert bitcoin.msg_prefix == b'\x18Bitcoin Signed Message:\n'
    assert bitcoin.min_tx_fee == 0
    assert bitcoin.min_vout_value == 0
    assert bitcoin.tx_timestamp == False
    assert bitcoin.denomination == Decimal('1e8')
    assert bitcoin.is_testnet == False
