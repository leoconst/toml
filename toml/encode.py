import functools
import itertools
from collections.abc import Mapping, Sequence
from datetime import datetime, date, time


@functools.singledispatch
def encoded(value):
    raise TypeError(f'Invalid encoding type: {type(value)}')


@encoded.register(str)
def encoded_str(value):
    value = repr(value)[1:-1]
    value = value.replace('"', '\\"')
    return '"' + value + '"'


@encoded.register(int)
@encoded.register(float)
def encoded_number(value):
    return str(value)


@encoded.register(bool)
def encoded_bool(value):
    return 'true' if value else 'false'


@encoded.register(datetime)
def encoded_datetime(value):
    iso_format = value.isoformat()
    return iso_format if value.tzinfo is None else iso_format + 'Z'


@encoded.register(date)
@encoded.register(time)
def encoded_date_or_time(value):
    return value.isoformat()


@encoded.register(Sequence)
def encoded_sequence(value):
    if not value:
        return '[]'
    return '[ ' + ', '.join(map(encoded, value)) + ' ]'


def encoded_key(key):
    if '.' in key:
        return encoded_str(key)
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


def encoded_mapping(mapping, _parent_title=''):
    lines = []
    add_line = lines.append

    # Encode all keys in the given mapping.
    encoded_keys = ((encoded_key(key), val) for key, val in mapping.items())
    # Separate the pairs into key-value pairs and tables.
    key_value_pairs, tables = partition(sort_item, encoded_keys)

    for key, value in key_value_pairs:
        add_line(f'{key} = {encoded(value)}')

    # Separate key-value pairs from tables with a blank line.
    add_line('')

    for key, value in tables:
        title = _parent_title + key
        # Add table header.
        add_line('[' + title + ']')
        add_line(encoded_mapping(value, title + '.'))

    return '\n'.join(lines)


def to_string(mapping):
    return encoded_mapping(mapping)


def to_path(path, mapping):
    """ Write the given mapping to a file at the given path
    """
    with open(path) as stream:
        stream.write(to_string(mapping))
