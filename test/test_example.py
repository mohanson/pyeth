import subprocess


def call(c: str):
    return subprocess.run(c, check=True, shell=True)


def test_addr():
    call('python example/addr.py --prikey 0x1')


def test_balance():
    call('python example/balance.py --addr 0x7e5f4552091a69125d5dfcb7b8c2659029395bdf')


def test_collision():
    call('python example/collision.py')


def test_scan_erc20():
    call('python example/scan_erc20.py')


def test_scan_eth():
    call('python example/scan_eth.py')


def test_storage():
    call('python example/storage.py --action deploy --prikey 0x1')
    call('python example/storage.py --action set --addr 0x930b793f778bbf43fab1080abf1840e018831cde --prikey 0x1')
    call('python example/storage.py --action get --addr 0x930b793f778bbf43fab1080abf1840e018831cde')


def test_transfer():
    call('python example/transfer.py --prikey 0x1 --to 0x2b5ad5c4795c026514f8317c7a215e218dccd6cf --value 0.05')
