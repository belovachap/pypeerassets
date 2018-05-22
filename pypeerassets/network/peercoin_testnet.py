from decimal import Decimal

from pypeerassets.network.network import Network


class PeercoinTestnet(Network):

    @property
    def name(self):
        return "peercoin-testnet"

    @property
    def short_name(self):
        return "tppc"

    @property
    def pub_key_hash(self):
        return b'6f'

    @property
    def wif_prefix(self):
        return b'ef'

    @property
    def script_hash(self):
        return b'c4'

    @property
    def magic_bytes(self):
        return b'cbf2c0ef'

    @property
    def msg_prefix(self):
        return b'\x17PPCoin Signed Message:\n'

    @property
    def min_tx_fee(self):
        return Decimal(0.01)

    @property
    def min_vout_value(self):
        return 0

    @property
    def tx_timestamp(self):
        return True

    @property
    def denomination(self):
        return Decimal('1e6')

    @property
    def is_testnet(self):
        return True

    def is_valid_address(self, address):
        raise NotImplementedError
