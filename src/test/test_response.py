import pytest

from rs500reader.do import Response, TempHum


def test_response_object():
    r = Response()
    r.set_channel_data(1, TempHum(23.4, 52))
    r.set_channel_data(3, TempHum(-1.4, 25))
    r.set_channel_data(6, TempHum(0.1, 78))
    assert 23.4 == r.get_channel_data(1).temperature
    assert 52 == r.get_channel_data(1).humidity
    assert -1.4 == r.get_channel_data(3).temperature
    assert 25 == r.get_channel_data(3).humidity
    assert 0.1 == r.get_channel_data(6).temperature
    assert 78 == r.get_channel_data(6).humidity


def test_invalid_channel_set():
    r = Response()
    r.set_channel_data(71, TempHum(0.5, 50))
    assert 0.5 == r.get_channel_data(71).temperature
    assert 50 == r.get_channel_data(71).humidity


def test_none_fetch():
    r = Response()
    with pytest.raises(AttributeError):
        dummy = r.get_channel_data(1).humidity


def test_get_all():
    th = TempHum(8.8, 76)
    r = Response()
    r.set_channel_data(2, th)
    assert {1: None, 2: th, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None} == r.all
