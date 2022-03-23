from typing import Sequence

import pytest

from rs500reader.do import TempHum


@pytest.mark.parametrize(
    "temp_from_protocol,expected_temp",
    [
        ([0x00, 0x00], 0),
        ([0xFF, 0xFF], -0.1),
        ([0xFF, 0xEE], -1.8),
        ([0xFF, 0xE7], -2.5),
        ([0x00, 0xCB], 20.3),
        ([0x00, 0xFF], 25.5),
        ([0x7F, 0xFF], 3276.7),  # Protocol Dumbness
    ],
)
def test_temp_parser(temp_from_protocol: Sequence[int], expected_temp: float):
    """
    Simple Test of some different temp values coming from the protocol
    """
    obj = TempHum.from_protocol(temp_from_protocol, 0)
    assert expected_temp == obj.temperature


@pytest.mark.parametrize(
    "hum_from_protocol,expected_hum",
    [
        (0x00, 0),
        (0xFF, 255),  # Protocol Dumbness
        (0x01, 1),
        (0x35, 53),
        (0x34, 52),
        (0x28, 40),
        (0x2B, 43),
    ],
)
def test_hum_parser(hum_from_protocol: int, expected_hum: int):
    """
    Simple Test of some different humidity values coming from the protocol
    """
    obj = TempHum.from_protocol([0, 0], hum_from_protocol)
    assert expected_hum == obj.humidity


def test_setters():
    """
    Check the property setters
    """
    obj = TempHum.from_protocol([0, 0], 0)
    assert obj.humidity == 0
    assert obj.temperature == 0
    obj.temperature = 23.4
    obj.humidity = 53
    assert obj.temperature == 23.4
    assert obj.humidity == 53
