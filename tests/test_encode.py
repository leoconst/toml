from datetime import datetime, date, time

import pytest

from common import augment_path, MAPPING, STRING
augment_path()

from toml.encode import encoded


def test_encode_str():
    assert encoded('') == '""'
    assert encoded('Hi my name jeff') == '"Hi my name jeff"'
    assert encoded('Tabs\ttabs\ttabs!') == r'"Tabs\ttabs\ttabs!"'
    assert encoded('''New
line''') == r'"New\nline"'


def test_encode_int():
    assert encoded(43) == '43'
    assert encoded(-21) == '-21'
    assert encoded(+3) == '3'


def test_encode_float():
    assert encoded(4.3) == '4.3'
    assert encoded(.9) == '0.9'
    assert encoded(-3.) == '-3.0'


def test_encode_bool():
    assert encoded(True) == 'true'
    assert encoded(False) == 'false'


def test_encode_datetime():
    dt = datetime(2132, 11, 3, 13, 37, 45)
    assert encoded(dt) == '2132-11-03T13:37:45'


def test_encode_mapping():
    assert encoded(MAPPING) == STRING


if __name__ == '__main__':
    pytest.main()
