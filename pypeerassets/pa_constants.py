'''various protocol constants'''

from collections import namedtuple
from decimal import Decimal


PAParams = namedtuple('PAParams', [
    'network_name',
    'network_shortname',
    'P2TH_wif',
    'P2TH_addr',
    'test_P2TH_wif',
    'test_P2TH_addr',
    'P2TH_fee',
])

params = (

    ## PPC mainnet
    PAParams("peercoin", "ppc", "U624wXL6iT7XZ9qeHsrtPGEiU78V1YxDfwq75Mymd61Ch56w47KE",
             "PAprodbYvZqf4vjhef49aThB9rSZRxXsM6", "UAbxMGQQKmfZCwKXAhUQg3MZNXcnSqG5Z6wAJMLNVUAcyJ5yYxLP",
             "PAtesth4QreCwMzXJjYHBcCVKbC4wjbYKP", Decimal(0.01)),

    ## PPC testnet
    PAParams("peercoin-testnet", "tppc", "cTJVuFKuupqVjaQCFLtsJfG8NyEyHZ3vjCdistzitsD2ZapvwYZH",
             "miHhMLaMWubq4Wx6SdTEqZcUHEGp8RKMZt", "cQToBYwzrB3yHr8h7PchBobM3zbrdGKj2LtXqg7NQLuxsHeKJtRL",
             "mvfR2sSxAfmDaGgPcmdsTwPqzS6R9nM5Bo", Decimal(0.01))
)


def param_query(query):
    '''find matching parameter among the networks'''

    for network in params:
        for field in network:
            if field == query:
                return network
