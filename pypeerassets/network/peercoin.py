from decimal import Decimal

from btcpy.structs.address import Address

from pypeerassets.network.network import Network


class Peercoin(Network):

    @property
    def name(self):
        return "peercoin"

    @property
    def short_name(self):
        return "ppc"

    @property
    def pub_key_hash(self):
        return b'37'

    @property
    def wif_prefix(self):
        return b'b7'

    @property
    def script_hash(self):
        return b'75'

    @property
    def magic_bytes(self):
        return b'e6e8e9e5'

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
        return False

    def is_valid_address(self, address):
        return Address.is_valid(address)
