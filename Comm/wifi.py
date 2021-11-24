import asyncio

import pyrcrack

async def scan_for_targets():
    """Scan targets 
    """
    airmon = pyrcrack.AirmonNg()
    print(type(airmon))
    dir(airmon)
    choices=[a['interface'] for a in await airmon.list_wifis]
    
    print(choices)
    async with airmon(interface) as mon:
        async with pyrcrack.AirodumpNg() as pdump:
            async for result in pdump(mon.monitor_interface):
                print(result.table)
                await asyncio.sleep(2)


asyncio.run(scan_for_targets())