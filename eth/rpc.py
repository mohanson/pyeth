import eth
import itertools
import random
import requests
import time
import typing

# Doc: https://ethereum.org/en/developers/docs/apis/json-rpc/


def call(method: str, params: typing.List) -> typing.Any:
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_block_number() -> str:
    return call('eth_blockNumber', [])


def eth_call(body: typing.Dict, block_number: str) -> str:
    return call('eth_call', [body, block_number])


def eth_chain_id() -> str:
    return call('eth_chainId', [])


def eth_estimate_gas(body: typing.Dict, block_number: str) -> str:
    return call('eth_estimateGas', [body, block_number])


def eth_gas_price() -> str:
    return call('eth_gasPrice', [])


def eth_get_balance(addr: str, block_number: str) -> str:
    return call('eth_getBalance', [addr, block_number])


def eth_get_block_by_hash(hash: str) -> typing.Dict:
    return call('eth_getBlockByHash', [hash, True])


def eth_get_block_by_number(block_number: str) -> typing.Dict:
    return call('eth_getBlockByNumber', [block_number, True])


def eth_get_block_transaction_count_by_hash(hash: str) -> str:
    return call('eth_getBlockTransactionCountByHash', [hash])


def eth_get_block_transaction_count_by_number(block_number: str) -> str:
    return call('eth_getBlockTransactionCountByNumber', [block_number])


def eth_get_code(addr: str, block_number: str) -> str:
    return call('eth_getCode', [addr, block_number])


def eth_get_transaction_by_hash(hash: str) -> typing.Dict:
    return call('eth_getTransactionByHash', [hash])


def eth_get_transaction_count(addr: str, block_number: str) -> str:
    return call('eth_getTransactionCount', [addr, block_number])


def eth_get_transaction_receipt(hash: str) -> typing.Dict:
    return call('eth_getTransactionReceipt', [hash])


def eth_max_priority_fee_per_gas() -> str:
    return call('eth_maxPriorityFeePerGas', [])


def eth_send_raw_transaction(tx: typing.Dict) -> str:
    return call('eth_sendRawTransaction', [tx])


def wait(hash: str):
    for _ in itertools.repeat(0):
        time.sleep(1)
        r = eth_get_transaction_by_hash(hash)
        if not r:
            continue
        if not r['blockNumber']:
            continue
        r = eth_get_transaction_receipt(hash)
        if not r:
            continue
        if int(r['status'], 0) != 1:
            raise Exception(r['status'])
        break
