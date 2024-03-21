import argparse
import eth

# Calculate the address from a private key.

parser = argparse.ArgumentParser()
parser.add_argument('prikey', type=str, help='private key')
args = parser.parse_args()

base = 10
if args.prikey.startswith('0x'):
    base = 16

prikey = eth.core.PriKey(int(args.prikey, base))
pubkey = prikey.pubkey()
addr = pubkey.addr()
print(addr)
