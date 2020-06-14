#!/usr/bin/env python3

from os.path import dirname

from rs5002mqtt.saver import save_data_to_mqtt

if __name__ == '__main__':
    to_save = {}
    to_save["ctest_temp"] = 20
    to_save["ctest_humi"] = 60
    save_data_to_mqtt(to_save, dirname(__file__) + '/' + 'check_rs500.ini' )
