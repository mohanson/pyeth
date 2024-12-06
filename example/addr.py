import argparse
import pleth

# Calculate the address from a private key.

parser = argparse.ArgumentParser()
parser.add_argument('--prikey', type=str, help='private key')
args = parser.parse_args()

prikey = pleth.core.PriKey(int(args.prikey, 0))
pubkey = prikey.pubkey()
addr = pubkey.addr()
print(f'0x{addr.hex()}')
