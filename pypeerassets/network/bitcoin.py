from decimal import Decimal

from pypeerassets.network.network import Network


class Bitcoin(Network):

    @property
    def name(self):
        return "bitcoin"

    @property
    def short_name(self):
        return "btc"

    @property
    def pub_key_hash(self):
        return b'00'

    @property
    def wif_prefix(self):
        return b'80'

    @property
    def script_hash(self):
        return b'05'

    @property
    def magic_bytes(self):
        return b'd9b4bef9'

    @property
    def msg_prefix(self):
        return b'\x18Bitcoin Signed Message:\n'

    @property
    def min_tx_fee(self):
        return 0

    @property
    def min_vout_value(self):
        return 0

    @property
    def tx_timestamp(self):
        return False

    @property
    def denomination(self):
        return Decimal('1e8')

    @property
    def is_testnet(self):
        return False

    def is_valid_address(self, address):
        raise NotImplementedError
