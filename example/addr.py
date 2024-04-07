import argparse
import eth

# Calculate the address from a private key.

parser = argparse.ArgumentParser()
parser.add_argument('--prikey', type=str, help='private key')
args = parser.parse_args()

prikey = eth.core.PriKey(int(args.prikey, 0))
pubkey = prikey.pubkey()
addr = pubkey.addr()
print(addr)
