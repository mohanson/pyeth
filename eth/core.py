import Crypto.Hash.keccak
import eth
import json


def hash(data: bytearray):
    k = Crypto.Hash.keccak.new(digest_bits=256)
    k.update(data)
    return bytearray(k.digest())


class PriKey:
    def __init__(self, n: int):
        self.n = n

    def __repr__(self):
        return json.dumps(self.json())

    def __eq__(self, other):
        a = self.n == other.n
        return a

    def json(self):
        return f'0x{self.n:064x}'

    def pubkey(self):
        pubkey = eth.secp256k1.G * eth.secp256k1.Fr(self.n)
        return PubKey(pubkey.x.x, pubkey.y.x)


class PubKey:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return json.dumps(self.json())

    def __eq__(self, other):
        a = self.x == other.x
        b = self.y == other.y
        return a and b

    def addr(self):
        b = bytearray()
        b.extend(self.x.to_bytes(32))
        b.extend(self.y.to_bytes(32))
        return '0x' + hash(b)[12:].hex()

    def json(self):
        return {
            'x': f'0x{self.x:064x}',
            'y': f'0x{self.y:064x}'
        }
