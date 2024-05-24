import argparse
import eth
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('--action', type=str, choices=['deploy', 'set', 'get'])
parser.add_argument('--addr', type=str, help='addr')
parser.add_argument('--net', type=str, choices=['develop'], default='develop')
parser.add_argument('--prikey', type=str, help='private key')
args = parser.parse_args()

if args.net == 'develop':
    eth.config.upgrade('http://127.0.0.1:8545')
    eth.config.current = eth.config.develop

if args.action == 'deploy':
    user = eth.wallet.Wallet(int(args.prikey, 0))
    data = bytearray(pathlib.Path('res/storage').read_bytes())
    hash = user.contract_deploy(data)
    print(f'hash = 0x{hash.hex()}')
    eth.rpc.wait(f'0x{hash.hex()}')
    addr = user.contract_addr(hash)
    print(f'addr = 0x{addr.hex()}')

if args.action == 'set':
    user = eth.wallet.Wallet(int(args.prikey, 0))
    data = eth.abi.function_selector('set', ['uint256']) + eth.abi.argument_encoding([
        eth.abi.encode_uint256(42),
    ])
    hash = user.contract_exec(bytearray.fromhex(args.addr[2:]), 0, data)
    print(f'hash = 0x{hash.hex()}')

if args.action == 'get':
    data = eth.abi.function_selector('get', [])
    r = eth.rpc.eth_call({
        'to': args.addr,
        'input': f'0x{data.hex()}'
    }, 'latest')
    print(f'data = {r}')
