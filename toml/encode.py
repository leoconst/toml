import functools
from collections.abc import Mapping, Sequence
from datetime import datetime, date, time


@functools.singledispatch
def encode(value):
    raise TypeError(f'Invalid encoding type: {type(value)}')


@encode.register(str)
def _encode_str(value):
    value = repr(value)[1:-1]
    value = value.replace('"', '\\"')
    return '"' + value + '"'


@encode.register(int)
@encode.register(float)
def _encode_number(value):
    return str(value)


@encode.register(bool)
def _encode_bool(value):
    return 'true' if value else 'false'


@encode.register(datetime)
def _encode_datetime(value):
    iso_format = value.isoformat()
    return iso_format if value.tzinfo is None else iso_format + 'Z'


@encode.register(date)
@encode.register(time)
def _encode_date_or_time(value):
    return value.isoformat()


@encode.register(Sequence)
def _encode_sequence(value):
    if not value:
        return '[]'
    return f"[ {', '.join(map(encode, value))} ]"


def _encode_mapping(mapping, parent_title=''):

    lines = []
    append = lines.append

    for key, value in sorted(mapping.items(), key=_sort_item):
        key = _encoded_key(key)
        if isinstance(value, Mapping):
            title = parent_title + key
            append('\n[' + title + ']')
            append(_encode_mapping(value, title + '.'))
        else:
            append(key + ' = ' + encode(value))

    return '\n'.join(lines)


def to_string(mapping):
    return _encode_mapping(mapping)


def to_path(path, mapping):
    """ Write the given mapping to a file at the given path
    """
    with open(path) as stream:
        stream.write(to_string(mapping))


def _encoded_key(key):
    if '.' in key:
        return _encode_str(key)
    return key


def _sort_item(item):
    key, value = item
    return isinstance(value, Mapping)
