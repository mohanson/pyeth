import eth


def test_balance():
    user = eth.wallet.Wallet(1)
    assert user.balance() != 0
