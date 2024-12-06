import argparse
import pleth

# Transfer ether to other.

parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
parser.add_argument('--prikey', type=str, help='private key')
parser.add_argument('--to', type=str, help='to address')
parser.add_argument('--value', type=float, help='ether value')
args = parser.parse_args()

if args.net == 'develop':
    pleth.config.upgrade('http://127.0.0.1:8545')
    pleth.config.current = pleth.config.develop
if args.net == 'mainnet':
    pleth.config.current = pleth.config.mainnet
if args.net == 'testnet':
    pleth.config.current = pleth.config.testnet

user = pleth.wallet.Wallet(int(args.prikey, 0))
hole = bytearray.fromhex(args.to[2:])

hash = user.transfer(hole, int(args.value * pleth.denomination.ether))
print(f'0x{hash.hex()}')
