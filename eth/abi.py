import eth.core
import typing


def function_selector(name: str, args_type: typing.List[str]) -> bytearray:
    s = name + '(' + ','.join(args_type) + ')'
    return eth.core.hash(bytearray(s.encode()))[:4]


def function_call(name: str, args_type: typing.List[str], args: typing.List[int | bytearray]) -> bytearray:
    assert len(args_type) == len(args)
    s = function_selector(name, args_type)
    for t, v in zip(args_type, args):
        if t == 'address':
            assert isinstance(v, bytearray)
            assert len(v) == 20
            s.extend(bytearray(12))
            s.extend(v)
            continue
        if t == 'uint256':
            assert isinstance(v, int)
            s.extend(bytearray(v.to_bytes(32)))
            continue
        raise Exception
    return s
