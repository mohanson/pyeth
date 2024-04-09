import eth
import json


class Wallet:
    def __init__(self, prikey: int):
        self.prikey = eth.core.PriKey(prikey)
        self.pubkey = self.prikey.pubkey()
        self.addr = self.pubkey.addr()

    def __repr__(self):
        return json.dumps(self.json())

    def __eq__(self, other):
        a = self.prikey == other.prikey
        return a

    def json(self):
        return {
            'prikey': self.prikey.json(),
            'pubkey': self.pubkey.json(),
            'addr': f'0x{self.addr.hex()}',
        }

    def balance(self):
        return int(eth.rpc.eth_get_balance(f'0x{self.addr.hex()}', 'latest'), 0)

    def contract_addr(self, hash: bytearray):
        return bytearray.fromhex(eth.rpc.eth_get_transaction_receipt(f'0x{hash.hex()}')['contractAddress'][2:])

    def contract_deploy(self, data: bytearray):
        gas_price = int(eth.rpc.eth_gas_price(), 0)
        gas = 21000 * 100
        value = 0
        tx = eth.core.TxLegacy(self.nonce(), gas_price, gas, None, value, data)
        return self.send(tx)

    def nonce(self):
        return int(eth.rpc.eth_get_transaction_count(f'0x{self.addr.hex()}', 'pending'), 0)

    def send(self, tx: eth.core.TxLegacy):
        tx.sign(self.prikey)
        hash = eth.rpc.eth_send_raw_transaction(f'0x{tx.rlp().hex()}')
        assert tx.hash() == bytearray.fromhex(hash[2:])
        return tx.hash()

    def transfer(self, addr: bytearray, value: int):
        gas_price = int(eth.rpc.eth_gas_price(), 0)
        gas = 21000
        tx = eth.core.TxLegacy(self.nonce(), gas_price, gas, addr, value, bytearray())
        return self.send(tx)

    def transfer_all(self, addr: bytearray):
        gas_price = int(eth.rpc.eth_gas_price(), 0)
        gas = 21000
        value = self.balance() - gas * gas_price
        tx = eth.core.TxLegacy(self.nonce(), gas_price, gas, addr, value, bytearray())
        return self.send(tx)
