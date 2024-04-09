import eth


def test_balance():
    user = eth.wallet.Wallet(1)
    assert user.balance() != 0


def test_transfer():
    user = eth.wallet.Wallet(1)
    hole = eth.wallet.Wallet(2)
    a = hole.balance()
    hash = user.transfer(hole.addr, 1 * eth.denomination.ether)
    eth.rpc.eth_wait(f'0x{hash.hex()}')
    b = hole.balance()
    assert b == a + 1 * eth.denomination.ether


def test_transfer_all():
    user = eth.wallet.Wallet(1)
    hole = eth.wallet.Wallet(2)
    hash = user.transfer(hole.addr, 1 * eth.denomination.ether)
    eth.rpc.eth_wait(f'0x{hash.hex()}')
    hash = hole.transfer_all(user.addr)
    eth.rpc.eth_wait(f'0x{hash.hex()}')
    assert hole.balance() == 0
