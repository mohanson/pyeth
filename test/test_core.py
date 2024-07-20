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


def test_text_hash():
    text = eth.core.Text('Hello Joe')
    assert text.hash().hex() == 'a080337ae51c4e064c189e113edd0ba391df9206e2f49db658bb32cf2911730b'


def test_sign():
    prikey = eth.core.PriKey(1)
    pubkey = prikey.pubkey()
    text = eth.core.Text('Hello Joe')
    assert text.pubkey(text.sign(prikey)) == pubkey
