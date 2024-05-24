import subprocess


def call(c: str):
    return subprocess.run(c, check=True, shell=True)


def test_addr():
    call('python example/addr.py --prikey 1')


def test_balance():
    call('python example/balance.py --addr 0x7e5f4552091a69125d5dfcb7b8c2659029395bdf')


def test_scan_block():
    call('python example/scan_block.py')


def test_storage():
    call('python example/storage.py --action deploy --prikey 1')
    call('python example/storage.py --action set --addr 0x930b793f778bbf43fab1080abf1840e018831cde --prikey 1')
    call('python example/storage.py --action get --addr 0x930b793f778bbf43fab1080abf1840e018831cde')
