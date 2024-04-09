# Python SDK for ETH

Python ETH is an experimental project that aims to provide human-friendly interfaces for common ETH operations. Note that Python ETH is not a complete SDK, but only implements the ETH functions that I am interested in.

## Installation

```sh
$ git clone https://github.com/mohanson/pyeth
$ cd pyeth
$ python -m pip install . --editable
```

## Usage

**example/addr.py**

Calculate the address from a private key.

```sh
$ python example/addr.py --prikey 0x0000000000000000000000000000000000000000000000000000000000000001

# 0x7e5f4552091a69125d5dfcb7b8c2659029395bdf
```

**example/balance.py**

Get the balance by an address.

```sh
$ python example/balance.py --addr 0x7e5f4552091a69125d5dfcb7b8c2659029395bdf

# 39934.9989371221
```

**example/storage.py**

Publish a storage contract, then store a number 42 in the contract, and finally read this number.

```sh
$ python example/storage.py --action deploy --prikey 1
# hash = 0xc4a663c8a867d1d6fcbb8b57794eb732baa1bf6cb4c1b0c1cee278e00c8fd644
# addr = 0x930b793f778bbf43fab1080abf1840e018831cde

$ python example/storage.py --action set --addr 0x930b793f778bbf43fab1080abf1840e018831cde --prikey 1
# hash = 0x95c3fab08f6f4dcac14db157c2c2936417ae528acf9637fd50f772ac617072b5

$ python example/storage.py --action get --addr 0x930b793f778bbf43fab1080abf1840e018831cde
# data = 0x000000000000000000000000000000000000000000000000000000000000002a
```

## Test

```sh
$ git clone https://github.com/ethereum/go-ethereum --branch release/1.13
$ cd go-ethereum
$ make geth

$ geth --dev --http
$ geth --exec "eth.sendTransaction({from: eth.accounts[0], to: '0x7e5f4552091a69125d5dfcb7b8c2659029395bdf', value: web3.toWei(10000, 'ether')})" attach /tmp/geth.ipc
$ pytest -v
```

## License

MIT
