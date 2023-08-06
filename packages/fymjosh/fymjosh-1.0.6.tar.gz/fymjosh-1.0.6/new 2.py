
try:
    import requests, threading, os, sys, time, asyncio, string, random, logging
    from requests.adapters import HTTPAdapter
    from getpass import getpass
    from colorama import Fore
    from pystyle import Write, System, Colorate, Colors
    
except:
    os.system('pip install asyncio')
    os.system('pip install requests')
    os.system('pip install colorama')

logging.basicConfig(
    level=logging.INFO,
    format="\033[38;5;196m[\033[0m%(asctime)s.%(msecs)03d\033[38;5;196m] \033[0m%(message)s\033[0m",
    datefmt="%H:%M:%S"
)

token = getpass("[>] Token: ")
guild_id = input("[>] Guild Id: ")
van_code = input("[>] Vanity Code: ")

class Sniper:
    def __init__(self):
        self.headers = {"Authorization": token}
        self.json = {"code": van_code}
        self.session = requests.Session()
        self.session.mount("", HTTPAdapter(max_retries=1))
        
        self.not_sniped = True
        
        self.heads = [
        {
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0'
        },

        {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
        },

        {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
        },

        {
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
        },

        {
            "Content-Type": "application/json",
             "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0"
        },

        {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
]

    def getheaders(self):
        headers = random.choice(self.heads)
        
        return headers
    
    def change_van(self):
        base = f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url"
        response = self.session.patch(url=base, headers=self.headers, json=self.json)
        try:
            if response.status_code == 200:
                logging.info(f" VANITY PROTECTED : https://discord.gg/{van_code} is now yours")
                
                os._exit(0)
            else:
                logging.info(f"COULDN'T PROTECT : for some odd reasoon couldn't snipe discord.gg/{van_code}")
        
        
        except:
            logging.info(f"Response from vanity change: {response.status_code}")
            
            
    def sniper(self):
        url = f"https://discord.com/api/v9/invites/{van_code}?with_counts=true&with_expiration=true"
        
        res = self.session.get(url=url, timeout=5, headers = self.getheaders())
        try:
            if res.status_code == 404:
                logging.info(f" VANITY IS NOT SAFE : https://discord.gg/{van_code} was just dropped...changing it")
                self.change_van()
                
            elif res.status_code == 200:
               
                time.sleep(1.3)
                self.sniper()
                
            elif res.status_code == 429:
                logging.info(f"RATELIMITED : You sent way too many requests suffering from ratelimits")
                b = res.json()
                time.sleep(0.6)
                self.sniper()
                
            else:
                logging.info(f"Status code : {res.status_code} - still taken")
                
        except:
            logging.info(f"Response from vanity sniper: {res.status_code}")
            
            
    def start(self):
        print("""
        
        
        
        """)
        while self.not_sniped:
            self.sniper()
         
        
        
        
        
if __name__ == "__main__":
    Sniper().start()