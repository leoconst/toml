import sys
from datetime import datetime, date, time
from pathlib import Path


def augment_path():
    sys.path.insert(0, str(Path(__file__).parent.parent))


MAPPING = {
    'foo': 2,
    'table': {
        'foo': [1, 2, 3],
        'empty': (),
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
    'times': {
        'date': date(1999, 4, 20),
        'time': time(13, 37, 59),
        'datetime': datetime(1, 2, 3, 4, 5, 6),
    },
    'bar': 3.2,
    'special': {
        'infinity': float('inf'),
        'neg-inf': float('-inf'),
        'not-a-number': float('nan'),
    },
}

STRING = '''\
foo = 2
bar = 3.2

[table]
foo = [ 1, 2, 3 ]
empty = []
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

[times]
date = 1999-04-20
time = 13:37:59
datetime = 0001-02-03T04:05:06

[special]
infinity = inf
neg-inf = -inf
not-a-number = nan
'''
