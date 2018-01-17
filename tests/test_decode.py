import re

import pytest

from common import augment_path, MAPPING, STRING
augment_path()

from toml.decode import KEYWORD, INTEGER, DATETIME, from_string


@pytest.mark.parametrize('invalid', [
    'True',
    'False',
    '0',
    '1',
    '',
])
def test_invalid_bool(invalid):
    assert re.fullmatch(KEYWORD, invalid) is None


@pytest.mark.parametrize('valid', [
    '0',
    '432',
    '+20',
    '-301',
    '40_40',
    '-1_000_000',
    '5_4_3_2_1',
])
def test_valid_integer(valid):
    assert re.match(INTEGER, valid)[0] == valid


@pytest.mark.parametrize('invalid', [
    '01',
    '-0004',
    '+01001',
    '-',
    '+',
    '+-',
    '0_1',
    '0_0_0',
    '1_000_',
    '1__0',
    '632_',
    '0___',
    '4____',
    '',
])
def test_invalid_integer(invalid):
    assert re.fullmatch(INTEGER, invalid) is None


@pytest.mark.parametrize('valid', [
    '1979-05-27T07:32:00Z',
    '1979-05-27T00:32:00-07:00',
    '1979-05-27T00:32:00.999999-07:00',
])
def test_valid_datetime(valid):
    assert re.match(DATETIME, valid)[0] == valid


if __name__ == '__main__':
    pytest.main()
