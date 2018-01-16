from datetime import datetime, date, time

import pytest

from common import augment_path, MAPPING, STRING
augment_path()

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


def test_encode_mapping():
    assert to_string(MAPPING) == STRING


if __name__ == '__main__':
    pytest.main()
