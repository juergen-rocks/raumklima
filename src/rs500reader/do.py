from typing import Sequence, Optional


class TempHum(object):

    def __init__(self, temp: float, hum: int):
        self.__temperature = temp
        self.__humidity = hum

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, temp: float):
        self.__temperature = temp

    @property
    def humidity(self):
        return self.__humidity

    @humidity.setter
    def humidity(self, hum: int):
        self.__humidity = hum

    @staticmethod
    def from_protocol(temp: Sequence[int], hum: int) -> 'TempHum':
        return TempHum(float(int.from_bytes(temp, byteorder='big', signed=True)) / 10.0, hum)


class Response(object):

    def __init__(self):
        self.__data = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None
        }

    def get_channel_data(self, channel: int) -> Optional[TempHum]:
        return self.__data[channel]

    def set_channel_data(self, channel: int, data: TempHum):
        self.__data[channel] = data

    @property
    def all(self) -> dict:
        return self.__data
