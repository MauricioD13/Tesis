import asyncio
from rich.console import Console
from rich.prompt import Prompt
import pyrcrack



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
asyncio.run(scan_for_targets())