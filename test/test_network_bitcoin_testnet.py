from decimal import Decimal

import pytest

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

def test_is_valid_address():
    """Check that the network can recognize valid addresses. NOTE: it's not
    currenlty implemented :(
    """
    bitcoin_testnet = BitcoinTestnet()
    with pytest.raises(NotImplementedError):
        bitcoin_testnet.is_valid_address("2NFNPUYRpDXf3YXEuVT6AdMesX4kyeyDjtp")
