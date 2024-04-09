import argparse
import eth

# Get the balance by an address.

parser = argparse.ArgumentParser()
parser.add_argument('--addr', type=str, required=True, help='address')
parser.add_argument('--net', type=str, choices=['develop'], default='testnet')
args = parser.parse_args()

if args.net == 'develop':
    eth.config.upgrade('http://127.0.0.1:8114')
    eth.config.current = eth.config.develop

balance = int(eth.rpc.eth_get_balance(args.addr, 'latest'), 0)
print(balance / eth.denomination.ether)
