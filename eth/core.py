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
        # https://ethereum.github.io/yellowpaper/paper.pdf, Appendix F. Signing Transactions.
        # We declare that an ECDSA signature is invalid unless all the following conditions are true:
        # 1) 0 < r < secp256k1n
        # 2) 0 < s < secp256k1n / 2 + 1
        # 3) v ∈ {0, 1}
        # There is only a small probability that v will get 2 and 3.
        if v > 1:
            return self.sign(data)
        # Here we adjust the sign of s.
        # Doc: https://ethereum.stackexchange.com/questions/55245/why-is-s-in-transaction-signature-limited-to-n-21
        if s.x * 2 >= eth.secp256k1.N:
            s = -s
            v = 1 - v
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
        assert isinstance(data, bytearray)
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

    def __repr__(self):
        return json.dumps(self.json())

    def __eq__(self, other):
        return self.hash() == other.hash()

    def hash(self):
        return hash(self.rlp())

    def json(self):
        return {
            'nonce': self.nonce,
            'gas_price': self.gas_price,
            'gas': self.gas,
            'to': f'0x{self.to.hex()}' if self.to else None,
            'value': self.value,
            'data': f'0x{self.data.hex()}',
            'v': self.v,
            'r': self.r,
            's': self.s,
        }

    def rlp(self) -> bytearray:
        return eth.rlp.encode([
            eth.rlp.put_uint(self.nonce),
            eth.rlp.put_uint(self.gas_price),
            eth.rlp.put_uint(self.gas),
            self.to if self.to else bytearray(),
            eth.rlp.put_uint(self.value),
            self.data,
            eth.rlp.put_uint(self.v),
            eth.rlp.put_uint(self.r),
            eth.rlp.put_uint(self.s),
        ])

    def sign(self, prikey: PriKey):
        # EIP-155: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md
        sign = prikey.sign(hash(eth.rlp.encode([
            eth.rlp.put_uint(self.nonce),
            eth.rlp.put_uint(self.gas_price),
            eth.rlp.put_uint(self.gas),
            self.to if self.to else bytearray(),
            eth.rlp.put_uint(self.value),
            self.data,
            eth.rlp.put_uint(eth.config.current.chain_id),
            eth.rlp.put_uint(0),
            eth.rlp.put_uint(0),
        ])))
        self.r = int.from_bytes(sign[0x00:0x20])
        self.s = int.from_bytes(sign[0x20:0x40])
        self.v = sign[0x40] + 35 + eth.config.current.chain_id * 2
