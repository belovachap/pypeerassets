from pypeerassets.network.bitcoin import Bitcoin
from pypeerassets.network.bitcoin_testnet import BitcoinTestnet
from pypeerassets.network.peercoin import Peercoin
from pypeerassets.network.peercoin_testnet import PeercoinTestnet


NETWORKS = {
    "bitcoin": Bitcoin,
    "bitcoin-testnet": BitcoinTestnet,
    "peercoin": Peercoin,
    "peercoin-testnet": PeercoinTestnet,
}
