import eth


def test_block_number():
    assert int(eth.rpc.eth_block_number(), 0) != 0


def test_get_balance():
    addr = eth.core.PriKey(1).pubkey().addr()
    coin = eth.rpc.eth_get_balance(f'0x{addr.hex()}', 'latest')
    assert int(coin, 0) != 0
