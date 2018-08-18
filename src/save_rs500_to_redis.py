#!/usr/bin/env python3

from os.path import dirname

from rs5002redis.saver import save_data_to_redis
from rs500common.configuration import discover_config_file_by_name
from rs500reader.reader import Rs500Reader


def fetch_and_save():
    reader = Rs500Reader()
    data = reader.get_data()
    if data is not None:
        to_save = {}
        for channel, values in data.all.items():
            if values is not None:
                to_save['c{}_temp'.format(channel)] = values.temperature
                to_save['c{}_humi'.format(channel)] = values.humidity
        save_data_to_redis(to_save, discover_config_file_by_name('rs5002redis.ini', dirname(__file__)))


if __name__ == '__main__':
    fetch_and_save()
