from typing import Sequence

import pytest

from rs500reader.do import TempHum


@pytest.mark.parametrize('temp_from_protocol,expected_temp', [
    ([0x00, 0x00], 0),
    ([0xff, 0xff], -0.1),
    ([0xff, 0xee], -1.8),
    ([0xff, 0xe7], -2.5),
    ([0x00, 0xcb], 20.3),
    ([0x00, 0xff], 25.5),
    ([0x7f, 0xff], 3276.7),  # Protocol Dumbness
])
def test_temp_parser(temp_from_protocol: Sequence[int], expected_temp: float):
    obj = TempHum.from_protocol(temp_from_protocol, 0)
    assert expected_temp == obj.temperature


@pytest.mark.parametrize('hum_from_protocol,expected_hum', [
    (0x00, 0),
    (0xff, 255),  # Protocol Dumbness
    (0x01, 1),
    (0x35, 53),
    (0x34, 52),
    (0x28, 40),
    (0x2b, 43),
])
def test_hum_parser(hum_from_protocol: int, expected_hum: int):
    obj = TempHum.from_protocol([0, 0], hum_from_protocol)
    assert expected_hum == obj.humidity


def test_setters():
    obj = TempHum.from_protocol([0, 0], 0)
    assert 0 == obj.humidity
    assert 0 == obj.temperature
    obj.temperature = 23.4
    obj.humidity = 53
    assert 23.4 == obj.temperature
    assert 53 == obj.humidity
