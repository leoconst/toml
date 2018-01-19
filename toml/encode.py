import functools
import itertools
from collections.abc import Mapping, Sequence
from datetime import datetime, date, time


@functools.singledispatch
def encode(value):
    raise TypeError(f'Invalid encoding type: {type(value)}')


@encode.register(str)
def encode_str(value):
    value = repr(value)[1:-1]
    value = value.replace('"', '\\"')
    return '"' + value + '"'


@encode.register(int)
@encode.register(float)
def encode_number(value):
    return str(value)


@encode.register(bool)
def encode_bool(value):
    return 'true' if value else 'false'


@encode.register(datetime)
def encode_datetime(value):
    iso_format = value.isoformat()
    return iso_format if value.tzinfo is None else iso_format + 'Z'


@encode.register(date)
@encode.register(time)
def encode_date_or_time(value):
    return value.isoformat()


@encode.register(Sequence)
def encode_sequence(value):
    if not value:
        return '[]'
    return '[ ' + ', '.join(map(encode, value)) + ' ]'


def encoded_key(key):
    if '.' in key:
        return encode_str(key)
    return key


def partition(predicate, iterable):
    """ Use a predicate to partition entries into False entries and True
    entries.
    >>> [tuple(it) for it in partition(lambda x: x % 2, range(10))]
    [(0, 2, 4, 6, 8), (1, 3, 5, 7, 9)]
    """
    t1, t2 = itertools.tee(iterable)
    return itertools.filterfalse(predicate, t1), filter(predicate, t2)


def sort_item(item):
    key, value = item
    return isinstance(value, Mapping)


def encode_mapping(mapping, parent_title=''):
    lines = []
    add_line = lines.append

    # Encode all keys in the given mapping.
    pairs = ((encoded_key(key), value) for key, value in mapping.items())
    # Separate the pairs into encoding values and tables.
    global_pairs, tables = partition(sort_item, pairs)

    for key, value in global_pairs:
        add_line(f'{key} = {encode(value)}')

    add_line('')

    for key, value in tables:
        title = parent_title + key
        add_line('[' + title + ']')
        add_line(encode_mapping(value, title + '.'))

    return '\n'.join(lines)


def to_string(mapping):
    return encode_mapping(mapping)


def to_path(path, mapping):
    """ Write the given mapping to a file at the given path
    """
    with open(path) as stream:
        stream.write(to_string(mapping))
