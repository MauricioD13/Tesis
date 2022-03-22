import os
import subprocess as sp
import asyncio

"""
Todos los comandos tiene su propia clase, y el atributo
command contiene el comando que se ingresará a la terminal
    Returns:
        _type_: _description_
"""


class Airmon:
    def __init__(self, interface):
        self.interface = interface
        self.command = 'airmon-ng'

    def monitor_mode(self):
        out = sp.check_output([self.command, 'start', self.interface])
        print(out)


class Airodump:
    def __init__(self, interface):
        self.interface = interface
        self.command = 'airodump-ng'

    def general_scan(self):
        out = sp.check_output(
            [self.command, '--output-format', 'csv', '-w', 'general_scan', self.interface])

    def AP_scan(self, channel, BSSID, AP_NAME):
        out = sp.check_output([self.command, '-c', channel, '--bssid',
                              BSSID, '-w', 'AP', self.interface])


class Aireplay:

    def __init__(self, ap, interface):
        self.ap = ap
        self.command = 'aireplay-ng'
        self.interface = interface

    def DDoS(self):
        out = sp.check_output([self.command, '-0', '20', '-a',
                               self.ap['AP_MAC'], self.interface])
        print(out)
        return 1
