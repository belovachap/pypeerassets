from abc import ABC, abstractmethod


class Network(ABC):

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def short_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def pub_key_hash(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def wif_prefix(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def script_hash(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def magic_bytes(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def msg_prefix(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def min_tx_fee(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def min_vout_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def tx_timestamp(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def denomination(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def is_testnet(self):
        raise NotImplementedError

    @abstractmethod
    def is_valid_address(self, address):
        raise NotImplementedError
