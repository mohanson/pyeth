import typing


def encode_byte(data: bytearray):
    body = bytearray()
    if len(data) == 0x01 and data[0] <= 0x7f:
        body.extend(data)
        return body
    if len(data) <= 0x37:
        body.append(0x80 + len(data))
        body.extend(data)
        return body
    if len(data):
        size = len(data).to_bytes()
        body.append(0xb7 + len(size))
        body.extend(size)
        body.extend(data)
        return body


def encode_list(data: typing.List[bytearray]):
    head = bytearray()
    body = bytearray()
    for e in data:
        body.extend(encode(e))
    if len(body) <= 0x37:
        head.append(0xc0 + len(body))
        return head + body
    if len(body):
        size = len(body).to_bytes()
        head.append(0xf7)
        head.extend(size)
        return head + body


def encode(data: bytearray | typing.List[bytearray]):
    if isinstance(data, bytearray):
        return encode_byte(data)
    if isinstance(data, list):
        return encode_list(data)


def decode_byte(data: bytearray):
    head = data[0]
    assert head <= 0xbf
    if head <= 0x7f:
        assert len(data) == 1
        body = data.copy()
        return body
    if head <= 0xb7:
        size = head - 0x80
        assert len(data) == 1 + size
        body = data[1:].copy()
        return body
    if head <= 0xbf:
        nlen = head - 0xb7
        size = int.from_bytes(data[1:1+nlen])
        assert len(data) == 1 + nlen + size
        body = data[1+nlen:].copy()
        return body


def decode_list(data: bytearray):
    head = data[0]
    assert head >= 0xc0
    offs = 0
    body = []
    if offs == 0 and head <= 0xf7:
        size = head - 0xc0
        assert len(data) == 1 + size
        offs += 1
    if offs == 0 and head <= 0xff:
        nlen = head - 0xf7
        size = int.from_bytes(data[1:1+nlen])
        assert len(data) == 1 + nlen + size
        offs += 1
        offs += nlen
    for _ in range(1 << 0xf):
        if offs >= len(data):
            break
        head = data[offs]
        if head < 0x80:
            body.append(decode_byte(data[offs: offs+1]))
            offs += 1
            continue
        if head < 0xb8:
            size = head - 0x80
            body.append(decode_byte(data[offs: offs+1+size]))
            offs += 1
            offs += size
            continue
        if head < 0xc0:
            nlen = head - 0xb7
            size = int.from_bytes(data[offs+1:offs+1+nlen])
            body.append(decode_byte(data[offs: offs+1+nlen+size]))
            offs += 1
            offs += nlen
            offs += size
            continue
        if head < 0xf8:
            size = head - 0xc0
            body.append(decode_list(data[offs: offs+1+size]))
            offs += 1
            offs += size
            continue
        if head:
            nlen = head - 0xf7
            size = int.from_bytes(data[offs+1:offs+1+nlen])
            body.append(decode_list(data[offs: offs+1+nlen+size]))
            offs += 1
            offs += nlen
            offs += size
            continue
    return body


def decode(data: bytearray):
    if data[0] <= 0xbf:
        return decode_byte(data)
    if data[0]:
        return decode_list(data)


def get_bool(data: bytearray):
    return len(data) == 1


def get_uint(data: bytearray):
    return int.from_bytes(data)


def put_bool(data: bool):
    return bytearray([0x01]) if data else bytearray()


def put_uint(data: int):
    return bytearray(data.to_bytes(32)).lstrip(bytearray([0x00]))
