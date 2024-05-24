import eth.core
import typing


def encode_uint256(data: int) -> bytearray:
    assert data >= 0
    assert data <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    return bytearray(data.to_bytes(32))


def decode_uint256(data: bytearray) -> int:
    assert len(data) == 32
    return int.from_bytes(data)


def encode_address(data: bytearray) -> bytearray:
    assert len(data) == 20
    return bytearray(12) + data


def decode_address(data: bytearray) -> bytearray:
    assert len(data) == 32
    return data[12:]


def function_selector(name: str, args_type: typing.List[str]) -> bytearray:
    s = name + '(' + ','.join(args_type) + ')'
    return eth.core.hash(bytearray(s.encode()))[:4]


def argument_encoding(data: typing.List[bytearray]) -> bytearray:
    s = bytearray()
    for e in data:
        s.extend(e)
    return s
