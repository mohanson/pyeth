import argparse
import eth

# Get the latest block and print out the transaction hash, sender, receiver and value(in ether).

parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, choices=['develop', 'mainnet'], default='develop')
args = parser.parse_args()

if args.net == 'develop':
    eth.config.upgrade('http://127.0.0.1:8545')
    eth.config.current = eth.config.develop
if args.net == 'mainnet':
    eth.config.current = eth.config.mainnet

block = eth.rpc.eth_get_block_by_number('latest')
for tx in block['transactions']:
    txhash = tx['hash']
    # Ethereum's transaction data does not contain the sender's address. Instead, you can calculate the sender's public
    # key from the transaction hash and signature, and then calculate the sender's address from the public key.
    m = int(txhash, 16)
    r = int(tx['r'], 16)
    s = int(tx['s'], 16)
    v = int(tx['v'], 16)
    # The value of V is very rich:
    # Legacy tx          : {0,1} + 27
    # Legacy tx + EIP-155: {0,1} + 35 + CHAIN_ID * 2
    # Other situations   : {0,1}
    if v > 26:
        v = v - 27 - eth.config.current.chain_id * 2
        v = v % 4
    pubkey = eth.ecdsa.pubkey(eth.secp256k1.Fr(m), eth.secp256k1.Fr(r), eth.secp256k1.Fr(s), v)
    sender = '0x' + eth.core.PubKey(pubkey.x.x, pubkey.y.x).addr().hex()
    accept = tx['to']
    amount = int(tx['value'], 16) / eth.denomination.ether
    print(f'{txhash} {sender} {accept} {amount}')
