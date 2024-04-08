import eth


def test_prikey():
    prikey = eth.core.PriKey(1)
    pubkey = prikey.pubkey()
    assert pubkey.x == 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    assert pubkey.y == 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8


def test_pubkey_addr():
    prikey = eth.core.PriKey(1)
    pubkey = prikey.pubkey()
    addr = pubkey.addr()
    assert addr.hex() == '7e5f4552091a69125d5dfcb7b8c2659029395bdf'
