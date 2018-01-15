from datetime import datetime, date, time

import pytest

from common import augment_path; augment_path()

from toml.encode import encode, to_string


def test_encode_str():
    assert encode('') == '""'
    assert encode('Hi my name jeff') == '"Hi my name jeff"'
    assert encode('Tabs\ttabs\ttabs!') == r'"Tabs\ttabs\ttabs!"'
    assert encode('''New
line''') == r'"New\nline"'


def test_encode_int():
    assert encode(43) == '43'
    assert encode(-21) == '-21'
    assert encode(+3) == '3'


def test_encode_float():
    assert encode(4.3) == '4.3'
    assert encode(.9) == '0.9'
    assert encode(-3.) == '-3.0'


def test_encode_bool():
    assert encode(True) == 'true'
    assert encode(False) == 'false'


def test_encode_datetime():
    dt = datetime(2132, 11, 3, 13, 37, 45)
    assert encode(dt) == '2132-11-03T13:37:45'


data = {
    'foo': 2,
    'table': {
        'foo': [1, 2, 3],
        'bar': -.3,
        'a': {
            'foo': 'Hello, I am a string.',
            'abc': list('abcdef'),
            'hash': {
                'yes': True,
                'no': False,
            },
        },
        'b.c': {
            'e': 5,
        },
        'time': datetime(432, 1, 5, 5, 32, 0),
        'list': [(4.1, 0.1), (3, 4, 1), (), (True, False)],
    },
    'bar': 3.2,
}

data_string = '''\
foo = 2
bar = 3.2

[table]
foo = [ 1, 2, 3 ]
bar = -0.3
time = 0432-01-05T05:32:00
list = [ [ 4.1, 0.1 ], [ 3, 4, 1 ], [], [ true, false ] ]

[table.a]
foo = "Hello, I am a string."
abc = [ "a", "b", "c", "d", "e", "f" ]

[table.a.hash]
yes = true
no = false

[table."b.c"]
e = 5
'''.rstrip()

def test_encode_mapping():
    assert to_string(data) == data_string


if __name__ == '__main__':
    pytest.main()
