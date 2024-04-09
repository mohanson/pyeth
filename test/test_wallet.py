import eth
import pathlib


def test_balance():
    user = eth.wallet.Wallet(1)
    assert user.balance() != 0


def test_contract_deploy():
    user = eth.wallet.Wallet(1)
    data = bytearray(pathlib.Path('res/storage').read_bytes())
    hash = user.contract_deploy(data)
    eth.rpc.eth_wait(f'0x{hash.hex()}')
    addr = user.contract_addr(hash)
    code = eth.rpc.eth_get_code(f'0x{addr.hex()}', 'latest')
    assert bytearray.fromhex(code[2:]) != bytearray()


def test_transfer():
    user = eth.wallet.Wallet(1)
    hole = eth.wallet.Wallet(2)
    a = hole.balance()
    hash = user.transfer(hole.addr, 1 * eth.denomination.ether)
    eth.rpc.eth_wait(f'0x{hash.hex()}')
    b = hole.balance()
    assert b == a + 1 * eth.denomination.ether


def test_transfer_all():
    user = eth.wallet.Wallet(1)
    hole = eth.wallet.Wallet(2)
    hash = user.transfer(hole.addr, 1 * eth.denomination.ether)
    eth.rpc.eth_wait(f'0x{hash.hex()}')
    hash = hole.transfer_all(user.addr)
    eth.rpc.eth_wait(f'0x{hash.hex()}')
    assert hole.balance() == 0
