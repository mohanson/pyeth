import eth

# Print all usdt transfer events in the last block.

eth.config.current = eth.config.mainnet

n = eth.rpc.eth_block_number()
r = eth.rpc.eth_get_logs({
    'fromBlock': n,
    'toBlock': n,
    'address': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'topics': [
        '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
    ]
})
for e in r:
    txhash = e['transactionHash'][2:]
    sender = '0x' + e['topics'][1][26:]
    accept = '0x' + e['topics'][2][26:]
    amount = int(e['data'], 16) / 1000000
    print(f'{txhash} {sender} {accept} {amount}')
