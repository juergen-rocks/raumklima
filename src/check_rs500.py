#!/usr/bin/env python3

import argparse

from os.path import dirname
from typing import Optional

from redis import StrictRedis, RedisError

from rs500common.configuration import ConfigProvider, discover_config_file_by_name

EXIT_CODE_OK = 0
EXIT_CODE_WARN = 1
EXIT_CODE_CRIT = 2
EXIT_CODE_UNKNOWN = 3

EXIT_WORD_OK = 'ok'
EXIT_WORD_WARN = 'warn'
EXIT_WORD_CRIT = 'CRITICAL'
EXIT_WORD_UNKNOWN = 'unknown'


def min_max_check(value, min_val, max_val) -> bool:
    if min_val is not None:
        if value < min_val:
            return False
    if max_val is not None:
        if value > max_val:
            return False
    return True


def check(args: argparse.Namespace, temp: Optional[float], humi: Optional[int]) -> int:
    output_format = '{{}}: {{}}; channel = {} -> temp = {}, humi = {}'.format(args.channel, temp, humi)

    if temp != 'unknown':
        if not min_max_check(temp, args.min_temp, args.max_temp):
            print(output_format.format(EXIT_WORD_CRIT, 'Temperature in critical range'))
            return EXIT_CODE_CRIT
        if not min_max_check(temp, args.min_warn_temp, args.max_warn_temp):
            print(output_format.format(EXIT_WORD_WARN, 'Temperature in warning range'))
            return EXIT_CODE_WARN
    if humi != 'unknown':
        if not min_max_check(humi, args.min_hum, args.max_hum):
            print(output_format.format(EXIT_WORD_CRIT, 'Humidity in critical range'))
            return EXIT_CODE_CRIT
        if not min_max_check(humi, args.min_warn_hum, args.max_warn_hum):
            print(output_format.format(EXIT_WORD_WARN, 'Humidity in warning range'))
            return EXIT_CODE_WARN

    print(output_format.format(EXIT_WORD_OK, 'everything fine'))
    return EXIT_CODE_OK


def handle_request(args: argparse.Namespace):
    conf = ConfigProvider(discover_config_file_by_name('check_rs500.ini', dirname(__file__))).get_config()
    host = conf.get(section='redis', option='host', fallback='localhost')
    port = conf.getint(section='redis', option='port', fallback=6379)
    db = conf.getint(section='redis', option='db', fallback=0)
    password = conf.getint(section='redis', option='password', fallback=None)
    prefix = conf.get(section='redis', option='prefix', fallback='')
    try:
        redis = StrictRedis(host=host, port=port, db=db, password=password)
        raw_value_temp = redis.get('{0}c{1}_temp'.format(prefix, args.channel))
        raw_value_humi = redis.get('{0}c{1}_humi'.format(prefix, args.channel))
        if raw_value_temp is None and raw_value_humi is None:
            print('{}: Unknown Channel [{}]'.format(EXIT_WORD_CRIT, args.channel))
            exit(2)
            return
        temp = 'unknown'
        humi = 'unknown'
        if raw_value_temp is not None:
            temp = float(bytes(raw_value_temp).decode())
        if raw_value_humi is not None:
            humi = int(bytes(raw_value_humi).decode())
        if any([args.min_temp is not None, args.max_temp is not None, args.min_warn_temp is not None, args.max_warn_temp is not None]) and raw_value_temp is None:
            print('{}: Should check temperature, but temperature is unknown; channel = {} -> temp = {}, humi = {}'.format(EXIT_WORD_CRIT, args.channel, temp, humi))
            exit(EXIT_CODE_CRIT)
            return
        if any([args.min_hum is not None, args.max_hum is not None, args.min_warn_hum is not None, args.max_warn_hum is not None]) and raw_value_humi is None:
            print('{}: Should check humidity, but humidity is unknown; channel = {} -> temp = {}, humi = {}'.format(EXIT_WORD_CRIT, args.channel, temp, humi))
            exit(EXIT_CODE_CRIT)
            return
        exit_code = check(args, temp, humi)
        exit(exit_code)
        return
    except RedisError:
        print('{}: Redis error'.format(EXIT_WORD_UNKNOWN))
        exit(EXIT_CODE_UNKNOWN)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='check_rs500', description='Hole RS500 Messwerte', epilog='Nutzbar als Icinga-Plugin')
    parser.add_argument('-c', '--channel', type=int, required=True, help='Kanal-Nummer (Pflicht)')
    parser.add_argument('--min-temp', type=float, help='Mindesttemperatur (numerische Werte) - Unterschreitung ist Critical')
    parser.add_argument('--max-temp', type=float, help='Maximalmaximaltemperatur (numerische Werte) - Überschreitung ist Critical')
    parser.add_argument('--min-warn-temp', type=float, help='Mindesttemperatur Warnung (numerische Werte) - Unterschreitung ist Warnung')
    parser.add_argument('--max-warn-temp', type=float, help='Maximaltemperatur Warnung (numerische Werte) - Überschreitung ist Warnung')
    parser.add_argument('--min-hum', type=int, help='Mindestluftfeuchte (numerische Werte) - Unterschreitung ist Critical')
    parser.add_argument('--max-hum', type=int, help='Maximalluftfeuchte (numerische Werte) - Überschreitung ist Critical')
    parser.add_argument('--min-warn-hum', type=int, help='Mindestluftfeuchte Warnung (numerische Werte) - Unterschreitung ist Warnung')
    parser.add_argument('--max-warn-hum', type=int, help='Maximalluftfeuchte Warnung (numerische Werte) - Überschreitung ist Warnung')
    handle_request(parser.parse_args())
