import argparse
import eth

# Transfer ether to other.

parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
parser.add_argument('--prikey', type=str, help='private key')
parser.add_argument('--to', type=str, required=True, help='to address')
parser.add_argument('--value', type=float, help='ether value')
args = parser.parse_args()

if args.net == 'develop':
    eth.config.upgrade('http://127.0.0.1:8545')
    eth.config.current = eth.config.develop
if args.net == 'mainnet':
    eth.config.current = eth.config.mainnet
if args.net == 'testnet':
    eth.config.current = eth.config.testnet

user = eth.wallet.Wallet(int(args.prikey, 0))
hole = bytearray.fromhex(args.to[2:])

hash = user.transfer(hole, int(args.value * eth.denomination.ether))
print(f'0x{hash.hex()}')
