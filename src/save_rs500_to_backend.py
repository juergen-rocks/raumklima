#!/usr/bin/env python3

"""
Get Values and save them to different backends
"""

from os.path import dirname

from rs500common.configuration import discover_config_file_by_name
from rs500common.configuration import ConfigProvider
from rs500reader.reader import Rs500Reader


def fetch_and_save():
    """
    Get Values from device and save them to those backends that are enabled in config file
    """

    config_file = discover_config_file_by_name("rs5002backend.ini", dirname(__file__))
    conf = ConfigProvider(config_file).get_config()
    enabled_redis = conf.get(section="redis", option="enabled", fallback="True").lower()
    enabled_mqtt = conf.get(section="mqtt", option="enabled", fallback="False").lower()

    reader = Rs500Reader()
    data = reader.get_data()
    if data is not None:
        to_save = {}
        for channel, values in data.all.items():
            if values is not None:
                to_save["c{}_temp".format(channel)] = values.temperature
                to_save["c{}_humi".format(channel)] = values.humidity
        if enabled_redis == "true":
            from rs5002redis.saver import save_data_to_redis

            save_data_to_redis(to_save, config_file)
        if enabled_mqtt == "true":
            from rs5002mqtt.saver import save_data_to_mqtt

            save_data_to_mqtt(to_save, config_file)


if __name__ == "__main__":
    fetch_and_save()
