import asyncio
from rich.console import Console
from rich.prompt import Prompt
import pyrcrack
import wifi_class as wifi


async def main():
    # wifi.Airmon(Prompt.ask('Select an interface',
    #              choices=))
    interface = 'wlp2s0'
    airmon = wifi.Airmon(interface)
    await airmon.monitor_mode()

    airodump = wifi.Airodump(interface)
    await airodump.general_scan()


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
asyncio.run(main())
