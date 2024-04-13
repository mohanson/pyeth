import eth
import itertools
import random
import requests
import time

# Doc: https://ethereum.org/en/developers/docs/apis/json-rpc/


def eth_block_number():
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_blockNumber',
        'params': []
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_call(body, block_number):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_call',
        'params': [body, block_number]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_chain_id():
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_chainId',
        'params': []
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_estimate_gas(body, block_number):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_estimateGas',
        'params': [body, block_number]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_gas_price():
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_gasPrice',
        'params': []
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_balance(addr, block_number):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getBalance',
        'params': [addr, block_number]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_block_by_hash(hash):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getBlockByHash',
        'params': [hash, True]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_block_by_number(block_number):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getBlockByNumber',
        'params': [block_number, True]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_block_transaction_count_by_hash(hash):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getBlockTransactionCountByHash',
        'params': [hash]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_block_transaction_count_by_number(block_number):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getBlockTransactionCountByNumber',
        'params': [block_number]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_code(addr, block_number):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getCode',
        'params': [addr, block_number]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_transaction_by_hash(hash):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getTransactionByHash',
        'params': [hash]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_transaction_count(addr, block_number):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getTransactionCount',
        'params': [addr, block_number]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_get_transaction_receipt(hash):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_getTransactionReceipt',
        'params': [hash]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_max_priority_fee_per_gas():
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_maxPriorityFeePerGas',
        'params': []
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_send_raw_transaction(tx):
    r = requests.post(eth.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': 'eth_sendRawTransaction',
        'params': [tx]
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def eth_wait(hash):
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
