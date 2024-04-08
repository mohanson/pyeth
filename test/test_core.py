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


def test_tx_legacy_hash():
    to = None
    tx = eth.core.TxLegacy(1, 12 * 10**9, 21000, to, 1 * 10**18, bytearray())
    assert tx.hash().hex() == '5a4e248363fd4d156668412ee21b4efb4d3b5036551252d2eb54ad2350ab4fd8'
    to = bytearray.fromhex('7e5f4552091a69125d5dfcb7b8c2659029395bdf')
    tx = eth.core.TxLegacy(1, 12 * 10**9, 21000, to, 1 * 10**18, bytearray())
    assert tx.hash().hex() == 'aa3dcc4217953cbd1df98823821376b32ecb6123fdfdfde84649c3373f2081e0'
    to = None
    tx = eth.core.TxLegacy(1, 12 * 10**9, 21000, to, 1 * 10**18, bytearray([0x00, 0x01]))
    assert tx.hash().hex() == '788498a80cfa16ac6b8d89cdc8d4dc0dfbfddd6667b1d27d54834ab1696a1bd1'
