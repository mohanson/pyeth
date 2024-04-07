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

## License

MIT
