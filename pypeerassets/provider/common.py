'''Common provider class with basic features.'''

from abc import ABC, abstractmethod
from decimal import Decimal
import urllib.request

from pypeerassets.exceptions import UnsupportedNetwork
from pypeerassets.network.network import Network
from pypeerassets.pa_constants import PAParams, param_query


class Provider(ABC):

    @abstractmethod
    def __init__(self, network: Network):
        '''Initialize a Provider.'''

        self._network = network

    @property
    def pa_parameters(self) -> PAParams:
        '''load network PeerAssets parameters.'''

        return param_query(self.network)

    @property
    @abstractmethod
    def network(self) -> Network:
        '''Return the Network object the Provider is using.'''

        return self._network

    @classmethod
    def sendrawtransaction(cls, rawtxn: str) -> dict:
        '''sendrawtransaction remote API
        :rawtxn - must be submitted as string'''

        if cls.is_testnet:
            url = 'https://testnet-explorer.peercoin.net/api/sendrawtransaction?hex={0}'.format(rawtxn)
        else:
            url = 'https://explorer.peercoin.net/api/sendrawtransaction?hex={0}'.format(rawtxn)

        resp = urllib.request.urlopen(url)
        return resp.read().decode('utf-8')

    @abstractmethod
    def getblockhash(self, blocknum: int) -> str:
        '''get blockhash using blocknum query'''
        raise NotImplementedError

    @abstractmethod
    def getblockcount(self) -> int:
        '''get block count'''
        raise NotImplementedError

    @abstractmethod
    def getblock(self, hash) -> dict:
        '''query block using <blockhash> as key.'''
        raise NotImplementedError

    @abstractmethod
    def getdifficulty(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def getbalance(self, address: str) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def getreceivedbyaddress(self, address: str) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def listunspent(self, address: str) -> list:
        raise NotImplementedError

    @abstractmethod
    def select_inputs(self, address: str, amount: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def getrawtransaction(self, txid: str, decrypt=1) -> dict:
        raise NotImplementedError

    @abstractmethod
    def listtransactions(self, address: str) -> list:
        raise NotImplementedError
