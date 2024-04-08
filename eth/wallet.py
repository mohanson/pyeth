import eth
import json


class Wallet:
    def __init__(self, prikey: int):
        self.prikey = eth.core.PriKey(prikey)
        self.pubkey = self.prikey.pubkey()
        self.addr = self.pubkey.addr()

    def __repr__(self):
        return json.dumps(self.json())

    def __eq__(self, other):
        a = self.prikey == other.prikey
        return a

    def json(self):
        return {
            'prikey': self.prikey.json(),
            'pubkey': self.pubkey.json(),
            'addr': f'0x{self.addr.hex()}',
        }

    def balance(self):
        return int(eth.rpc.eth_get_balance(f'0x{self.addr.hex()}', 'latest'), 0)
