import argparse
import pleth

# Get the balance by an address.

parser = argparse.ArgumentParser()
parser.add_argument('--addr', type=str, help='address')
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
args = parser.parse_args()

if args.net == 'develop':
    pleth.config.upgrade('http://127.0.0.1:8545')
    pleth.config.current = pleth.config.develop
if args.net == 'mainnet':
    pleth.config.current = pleth.config.mainnet
if args.net == 'testnet':
    pleth.config.current = pleth.config.testnet

balance = int(pleth.rpc.eth_get_balance(args.addr, 'latest'), 0)
print(balance / pleth.denomination.ether)
