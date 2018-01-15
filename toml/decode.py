import collections
import functools
import re
from collections.abc import Sequence
from datetime import datetime
from enum import Enum
from pathlib import Path


def combined_re(*regexes, escape=False):
    if escape:
        regexes = map(re.escape, regexes)
    return r'(' + r'|'.join(regexes) + r')'


COMMENT = r'#[^\n]*'
WHITESPACE = r'[ \t]+'
SKIP = combined_re(COMMENT, WHITESPACE)

BASIC_STRING = r'"[^\n]*?(?<!\\)"'
BASIC_STRING_MULTILINE = r'""".*?"""'

LITERAL_STRING = r"'[^\n]*?'"
LITERAL_STRING_MULTILINE = r"'''.*?'''"

BARE_KEY = r'[A-Za-z0-9_-]+'
KEY = combined_re(BARE_KEY, BASIC_STRING)

KEY_VALUE = KEY + r'[ \t]*='

TABLE_TITLE = fr'\[{KEY}(\.{KEY})*\]'

DIGITS = r'(([1-9]\d*(_\d+)*)|0)'
INTEGER = r'[-\+]?' + DIGITS
FLOAT = fr'{INTEGER}\.{DIGITS}|([Ee]{INTEGER})'

DATE = r'\d{4}-\d{2}-\d{2}'
TIME = r'\d{2}:\d{2}:\d{2}(\.\d{3,6})?'

DATETIME = DATE + r'[ Tt]' + TIME + r'(([\+\-]\d{2}:\d{2})|[Zz])'

KEYWORDS = {
    'true': True,
    'false': False,
    'inf': float('inf'),
    '+inf': float('+inf'),
    '-inf': float('-inf'),
    'nan': float('nan'),
    '+nan': float('+nan'),
    '-nan': float('-nan'),
}

KEYWORD = combined_re(*KEYWORDS, escape=True)


class Token(Enum):
    SKIP = SKIP
    LITERAL_STRING_MULTILINE = LITERAL_STRING_MULTILINE
    LITERAL_STRING = LITERAL_STRING
    BASIC_STRING_MULTILINE = BASIC_STRING_MULTILINE
    BASIC_STRING = BASIC_STRING
    TABLE_TITLE = TABLE_TITLE
    KEY_VALUE = KEY_VALUE
    DATETIME = DATETIME
    FLOAT = FLOAT
    INTEGER = INTEGER
    KEYWORD = KEYWORD
    ARRAY_START = r'\['
    ARRAY_END = r'\]'
    TABLE_START = r'\{'
    TABLE_END = r'\}'
    SEPARATOR = r','
    NEWLINE = r'\n'
    MISMATCH = r'[^\n]+'

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'


TOKENISE_RE = re.compile(
    r'|'.join(f'(?P<{token.name}>{token.value})' for token in Token), re.DOTALL
)


TokenInfo = collections.namedtuple('TokenInfo', 'enum, value')


class TOMLSyntaxError(SyntaxError):
    pass


def tokenize(source):
    """ Return an iterable of TokenInfo objects.
    """
    line_number = 1
    line_start = 0

    for match in TOKENISE_RE.finditer(source):

        enum = Token[match.lastgroup]

        if enum == Token.SKIP:
            continue
        if enum == Token.NEWLINE:
            line_number += 1
            line_start = match.end()

        value = match[0]
        column = match.start() - line_start

        if enum == Token.MISMATCH:
            print('mismatch:', match)
            raise TOMLSyntaxError('Invalid TOML',
                ('foo.toml', line_number, column, value))

        yield TokenInfo(enum, value)


def decode_float(value):
    if value[0].lower() == 'e':
        value = '0' + value
    return float(value)


def decode_datetime(value):
    return datetime.now()
    # return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')


def decode_literal_string(value):
    """ Remove one quote from each side of a string.
    """
    return value[1:-1]


def decode_literal_string_multiline(value):
    """ Remove triple quotes from each end of the string and trim a
    starting newline if present.
    """
    value = value[3:-3]
    if value.startswith('\n'):
        value = value[1:]
    return value


BASIC_STRING_ESCAPE_CHARS = (
    ('\\b', '\b'),
    ('\\t', '\t'),
    ('\\n', '\n'),
    ('\\f', '\f'),
    ('\\r', '\r'),
    ('\\"', '"'),
)


def escape_basic_string(string):
    for old, new in BASIC_STRING_ESCAPE_CHARS:
        string = string.replace(old, new)
    return string


def decode_basic_string(value):
    return escape_basic_string(decode_literal_string(value))


def decode_basic_string_multiline(value):
    value = decode_literal_string_multiline(value)
    value = escape_basic_string(value)
    # Trim whitespace after line ending backslashes.
    value = ''.join(segment.lstrip(' \n') for segment in value.split('\\\n'))
    return value


DECODE_FUNCTIONS = {
    Token.BASIC_STRING: decode_basic_string,
    Token.BASIC_STRING_MULTILINE: decode_basic_string_multiline,
    Token.LITERAL_STRING: decode_literal_string,
    Token.LITERAL_STRING_MULTILINE: decode_literal_string_multiline,
    Token.INTEGER: int,
    Token.FLOAT: decode_float,
    Token.KEYWORD: KEYWORDS.get,
    Token.DATETIME: decode_datetime,
}


def from_path(path):
    """ Load a mapping from a TOML file.
    """
    with open(path) as stream:
        source = stream.read()

    return from_string(source)


def from_string(string):
    """ Load a mapping from a TOML string.
    """
    table = current_table = {}

    tokens = tokenize(string)
    get_next_token = tokens.__next__

    for enum, value in tokens:
        if enum == Token.TABLE_TITLE:
            current_table = table[value[1:-1]] = {}
        elif enum == Token.KEY_VALUE:
            key = value.rstrip('\t =')
            enum, value = get_next_token()
            if enum not in (Token.TABLE_START, Token.ARRAY_START):
                current_table[key] = DECODE_FUNCTIONS[enum](value)

    return table
