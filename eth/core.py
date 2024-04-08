import Crypto.Hash.keccak
import eth
import json
import typing


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

    def sign(self, data: bytearray):
        assert len(data) == 32
        m = eth.secp256k1.Fr(int.from_bytes(data))
        r, s, v = eth.ecdsa.sign(eth.secp256k1.Fr(self.n), m)
        # Here we do not adjust the sign of s.
        # Doc: https://ethereum.stackexchange.com/questions/55245/why-is-s-in-transaction-signature-limited-to-n-21
        # For BTC, v is in the prefix.
        # For ETH, v is in the suffix.
        return bytearray(r.x.to_bytes(32)) + bytearray(s.x.to_bytes(32)) + bytearray([v])


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
        return hash(b)[12:]

    def json(self):
        return {
            'x': f'0x{self.x:064x}',
            'y': f'0x{self.y:064x}'
        }


class TxLegacy:
    def __init__(
        self,
        nonce: int,
        gas_price: int,
        gas: int,
        to: typing.Optional[bytearray],
        value: int,
        data: bytearray,
    ):
        self.nonce = nonce
        self.gas_price = gas_price
        self.gas = gas
        # None means contract creation.
        self.to = to
        self.value = value
        self.data = data
        # Signature values.
        self.v = 0
        self.r = 0
        self.s = 0

    def hash(self) -> bytearray:
        return hash(eth.rlp.encode([
            eth.rlp.put_uint(self.nonce),
            eth.rlp.put_uint(self.gas_price),
            eth.rlp.put_uint(self.gas),
            self.to if self.to else bytearray(),
            eth.rlp.put_uint(self.value),
            self.data,
            eth.rlp.put_uint(eth.config.current.chain_id),
            eth.rlp.put_uint(0),
            eth.rlp.put_uint(0),
        ]))
