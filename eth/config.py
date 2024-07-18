import random
import requests
import typing


class ObjectDict(dict):
    def __getattr__(self, name: str) -> typing.Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: typing.Any):
        self[name] = value


develop = ObjectDict({
    'url': 'http://127.0.0.1:8545',
    'chain_id': 1337,
    'tx_gas': 21000,
})

mainnet = ObjectDict({
    'url': 'https://eth.llamarpc.com',
    'chain_id': 1,
    'tx_gas': 21000,
})

testnet = ObjectDict({
    'url': 'https://rpc.sepolia.org',
    'chain_id': 11155111,
    'tx_gas': 21000,
})


def upgrade(url: str):
    develop.url = url
    develop.chain_id = int(requests.post(url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_chainId',
        'params': []
    }).json()['result'], 0)


current = develop
