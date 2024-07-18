import argparse
import eth
import random

# Generate a random private key and check whether there are assets under the private key.

parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
parser.add_argument('--limit', type=int, default=8, help='number of attempts')
args = parser.parse_args()

if args.net == 'develop':
    eth.config.upgrade('http://127.0.0.1:8545')
    eth.config.current = eth.config.develop
if args.net == 'mainnet':
    eth.config.current = eth.config.mainnet
if args.net == 'testnet':
    eth.config.current = eth.config.testnet

for _ in range(args.limit):
    prikey = eth.core.PriKey(random.randint(1, (1 << 256) - 1))
    pubkey = prikey.pubkey()
    addr = pubkey.addr()
    number = eth.rpc.eth_get_balance(f'0x{addr.hex()}', 'latest')
    print(prikey.json()['n'], number)
    if number != '0x0':
        break
