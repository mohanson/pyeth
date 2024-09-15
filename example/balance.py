import argparse
import eth

# Get the balance by an address.

parser = argparse.ArgumentParser()
parser.add_argument('--addr', type=str, help='address')
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
args = parser.parse_args()

if args.net == 'develop':
    eth.config.upgrade('http://127.0.0.1:8545')
    eth.config.current = eth.config.develop
if args.net == 'mainnet':
    eth.config.current = eth.config.mainnet
if args.net == 'testnet':
    eth.config.current = eth.config.testnet

balance = int(eth.rpc.eth_get_balance(args.addr, 'latest'), 0)
print(balance / eth.denomination.ether)
