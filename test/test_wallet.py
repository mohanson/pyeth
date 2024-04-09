import eth


def test_balance():
    user = eth.wallet.Wallet(1)
    assert user.balance() != 0


def test_transfer():
    user = eth.wallet.Wallet(1)
    hole = eth.wallet.Wallet(2)
    a = hole.balance()
    hash = user.transfer(hole.addr, 1 * 10**18)
    eth.rpc.eth_wait(f'0x{hash.hex()}')
    b = hole.balance()
    assert b == a + 1 * 10**18
