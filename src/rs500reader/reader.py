from sys import stderr
from typing import Optional

import hid
import time

from .do import Response, TempHum


class Rs500Reader(object):

    def __init__(self, vendor_id = 0x0483, product_id = 0x5750):
        self.__vendor = vendor_id
        self.__product = product_id

    def __query(self) -> Optional[bytes]:
        try:
            rs500_hid = hid.device()
            rs500_hid.open(self.__vendor, self.__product)
            rs500_hid.set_nonblocking(1)
            # Anfrage 04, liefert die Temperaturen und Luftfeuchten
            rs500_hid.write([0x7b, 0x03, 0x40, 0x7d] + [0] * 60)
            time.sleep(0.75)
            data = []
            while True:
                d = rs500_hid.read(64)
                if d:
                    data += d
                else:
                    break
            rs500_hid.close()
            return d
        except IOError as e:
            print(e, file=stderr)
            return None

    def get_data(self) -> Optional[Response]:
        data = self.__query()
        if len(data) != 64:
            print('ungültige Länge!', file=stderr)
            return None
        response = Response()
        channel = 0
        for i in range(start=1, step=3, stop=24):
            channel += 1
            t1 = data[i]
            t2 = data[i+1]
            hu = data[i+2]
            if t1 != 0x7f and t2 != 0xff and hu != 0xff:
                response.set_channel_data(channel, TempHum.from_protocol([t1, t2], hu))
        return response
