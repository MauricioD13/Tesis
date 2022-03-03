import csv
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import sys


def csv_handler(name):

    console = Console()
    with open(name, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        headers = next(reader)

        # Prompt options
        table = Table(show_header=True, header_style='bold magenta')
        table.add_column("Seleccion", width=12)
        table.add_column("BSSID", width=12)
        table.add_column("Channel", width=12)
        table.add_column("Speed", width=12)
        table.add_column("Privacy", width=12)
        table.add_column("Cipher", width=12)
        table.add_column("Authetication", width=12)
        table.add_column("ESSID", width=12)

        num = []
        index = 0
        info = {}
        for idx, value in enumerate(reader):

            try:
                table.add_row("["+str(idx)+"]", value[0], value[3],
                              value[4], value[5], value[6], value[7], value[13])
                info[idx] = (value[0], value[3],
                             value[4], value[5], value[6], value[7], value[13])
            except IndexError:
                index = idx
                break
            num.append(str(idx))

        console.print(table)
        option = int(Prompt.ask("Interfaz: ", choices=num))

        return info[option]
