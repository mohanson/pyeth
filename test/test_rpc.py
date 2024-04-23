import eth


def test_eth_block_number():
    assert int(eth.rpc.eth_block_number(), 0) != 0


def test_eth_get_balance():
    addr = eth.core.PriKey(1).pubkey().addr()
    coin = eth.rpc.eth_get_balance(f'0x{addr.hex()}', 'latest')
    assert int(coin, 0) != 0


def test_eth_max_priority_fee_per_gas():
    assert int(eth.rpc.eth_max_priority_fee_per_gas(), 0) != 0


def test_eth_send_raw_transaction_tx_access_list():
    user_prikey = eth.core.PriKey(1)
    user_addr = user_prikey.pubkey().addr()
    hole_prikey = eth.core.PriKey(2)
    hole_addr = hole_prikey.pubkey().addr()
    tx = eth.core.TxAccessList(
        eth.config.current.chain_id,
        int(eth.rpc.eth_get_transaction_count(f'0x{user_addr.hex()}', 'pending'), 0),
        int(eth.rpc.eth_gas_price(), 0),
        eth.config.current.tx_gas,
        hole_addr,
        1 * eth.denomination.ether,
        bytearray(),
    )
    tx.sign(user_prikey)
    val1 = int(eth.rpc.eth_get_balance(f'0x{hole_addr.hex()}', 'latest'), 0)
    hash = eth.rpc.eth_send_raw_transaction(f'0x{tx.envelope().hex()}')
    eth.rpc.wait(hash)
    val2 = int(eth.rpc.eth_get_balance(f'0x{hole_addr.hex()}', 'latest'), 0)
    assert val2 == val1 + 1 * eth.denomination.ether


def test_eth_send_raw_transaction_tx_dynamic_fee():
    user_prikey = eth.core.PriKey(1)
    user_addr = user_prikey.pubkey().addr()
    hole_prikey = eth.core.PriKey(2)
    hole_addr = hole_prikey.pubkey().addr()
    gas_tip_cap = int(eth.rpc.eth_max_priority_fee_per_gas(), 0)
    gas_pre = int(eth.rpc.eth_get_block_by_number('latest')['baseFeePerGas'], 0)
    gas_fee_cap = gas_pre + gas_tip_cap
    tx = eth.core.TxDynamicFee(
        eth.config.current.chain_id,
        int(eth.rpc.eth_get_transaction_count(f'0x{user_addr.hex()}', 'pending'), 0),
        gas_tip_cap,
        gas_fee_cap,
        eth.config.current.tx_gas,
        hole_addr,
        1 * eth.denomination.ether,
        bytearray(),
    )
    tx.sign(user_prikey)
    val1 = int(eth.rpc.eth_get_balance(f'0x{hole_addr.hex()}', 'latest'), 0)
    hash = eth.rpc.eth_send_raw_transaction(f'0x{tx.envelope().hex()}')
    eth.rpc.wait(hash)
    val2 = int(eth.rpc.eth_get_balance(f'0x{hole_addr.hex()}', 'latest'), 0)
    assert val2 == val1 + 1 * eth.denomination.ether


def test_eth_send_raw_transaction_tx_legacy():
    user_prikey = eth.core.PriKey(1)
    user_addr = user_prikey.pubkey().addr()
    hole_prikey = eth.core.PriKey(2)
    hole_addr = hole_prikey.pubkey().addr()
    tx = eth.core.TxLegacy(
        int(eth.rpc.eth_get_transaction_count(f'0x{user_addr.hex()}', 'pending'), 0),
        int(eth.rpc.eth_gas_price(), 0),
        eth.config.current.tx_gas,
        hole_addr,
        1 * eth.denomination.ether,
        bytearray(),
    )
    tx.sign(user_prikey)
    val1 = int(eth.rpc.eth_get_balance(f'0x{hole_addr.hex()}', 'latest'), 0)
    hash = eth.rpc.eth_send_raw_transaction(f'0x{tx.envelope().hex()}')
    eth.rpc.wait(hash)
    val2 = int(eth.rpc.eth_get_balance(f'0x{hole_addr.hex()}', 'latest'), 0)
    assert val2 == val1 + 1 * eth.denomination.ether
