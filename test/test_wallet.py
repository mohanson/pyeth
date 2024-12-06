import pathlib
import pleth


def test_balance():
    user = pleth.wallet.Wallet(1)
    assert user.balance() != 0


def test_contract_deploy():
    user = pleth.wallet.Wallet(1)
    data = bytearray(pathlib.Path('res/storage').read_bytes())
    hash = user.contract_deploy(data)
    pleth.rpc.wait(f'0x{hash.hex()}')
    addr = user.contract_addr(hash)
    code = pleth.rpc.eth_get_code(f'0x{addr.hex()}', 'latest')
    assert bytearray.fromhex(code[2:]) != bytearray()


def test_transfer():
    user = pleth.wallet.Wallet(1)
    hole = pleth.wallet.Wallet(2)
    a = hole.balance()
    hash = user.transfer(hole.addr, 1 * pleth.denomination.ether)
    pleth.rpc.wait(f'0x{hash.hex()}')
    b = hole.balance()
    assert b == a + 1 * pleth.denomination.ether


def test_transfer_all():
    user = pleth.wallet.Wallet(1)
    hole = pleth.wallet.Wallet(2)
    hash = user.transfer(hole.addr, 1 * pleth.denomination.ether)
    pleth.rpc.wait(f'0x{hash.hex()}')
    hash = hole.transfer_all(user.addr)
    pleth.rpc.wait(f'0x{hash.hex()}')
    assert hole.balance() == 0
