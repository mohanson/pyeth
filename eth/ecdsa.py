import eth.secp256k1
import itertools
import random


def sign(prikey: eth.secp256k1.Fr, m: eth.secp256k1.Fr) -> tuple[eth.secp256k1.Fr, eth.secp256k1.Fr, int]:
    # https://www.secg.org/sec1-v2.pdf
    # 4.1.3 Signing Operation
    for _ in itertools.repeat(0):
        k = eth.secp256k1.Fr(random.randint(0, eth.secp256k1.N - 1))
        R = eth.secp256k1.G * k
        r = eth.secp256k1.Fr(R.x.x)
        if r.x == 0:
            continue
        s = (m + prikey * r) / k
        if s.x == 0:
            continue
        v = 0
        if R.y.x & 1 == 1:
            v |= 1
        if R.x.x >= eth.secp256k1.N:
            v |= 2
        return r, s, v


def verify(pubkey: eth.secp256k1.Pt, m: eth.secp256k1.Fr, r: eth.secp256k1.Fr, s: eth.secp256k1.Fr) -> bool:
    # https://www.secg.org/sec1-v2.pdf
    # 4.1.4 Verifying Operation
    u1 = m / s
    u2 = r / s
    x = eth.secp256k1.G * u1 + pubkey * u2
    assert x != eth.secp256k1.I
    v = eth.secp256k1.Fr(x.x.x)
    return v == r


def pubkey(m: eth.secp256k1.Fr, r: eth.secp256k1.Fr, s: eth.secp256k1.Fr, v: int) -> eth.secp256k1.Pt:
    # https://www.secg.org/sec1-v2.pdf
    # 4.1.6 Public Key Recovery Operation
    assert v in [0, 1, 2, 3]
    if v & 2 == 0:
        x = eth.secp256k1.Fq(r.x)
    else:
        x = eth.secp256k1.Fq(r.x + eth.secp256k1.N)
    y_y = x * x * x + eth.secp256k1.A * x + eth.secp256k1.B
    y = y_y ** ((eth.secp256k1.P + 1) // 4)
    if v & 1 != y.x & 1:
        y = -y
    R = eth.secp256k1.Pt(x, y)
    return (R * s - eth.secp256k1.G * m) / r
