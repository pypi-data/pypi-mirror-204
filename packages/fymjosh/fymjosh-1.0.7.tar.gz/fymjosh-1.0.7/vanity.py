import discord
from discord.ext import commands
import logging
import asyncio
import requests
from pystyle import Anime, Colorate, Add, Colors, System, Center
from requests_futures.sessions import FuturesSession

logging.basicConfig(
    level=logging.INFO,
    format="\033[38;5;196m[\033[0m%(asctime)s.%(msecs)03d\033[38;5;196m] \033[0m%(message)s\033[0m",
    datefmt="%H:%M:%S"
)

MAX_WORKERS = 30

tok = input("Account Token: ")

TOKEN = "MTA3NjUyNDUyMTQzNzI4NjQ1Mg.GmS3Iq.Oqmp5b73eltTc1tk0VWk-xp_C5hJE7bF4i5njE"

guild_idss = ["1063925639528337408"]

client = commands.Bot(command_prefix=";", intents=discord.Intents.all(), help_command=None)


logo = Center.XCenter(r"""
██╗   ██╗ █████╗ ███╗   ██╗██╗████████╗██╗   ██╗    
██║   ██║██╔══██╗████╗  ██║██║╚══██╔══╝╚██╗ ██╔╝    
██║   ██║███████║██╔██╗ ██║██║   ██║    ╚████╔╝     
╚██╗ ██╔╝██╔══██║██║╚██╗██║██║   ██║     ╚██╔╝      
 ╚████╔╝ ██║  ██║██║ ╚████║██║   ██║      ██║       
  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝      ╚═╝       

""")

@client.event
async def on_ready():
    System.Clear()
    print(Colorate.Vertical(Colors.red_to_purple, logo))
    logging.info("Ready TO Protect")
    
    
@client.event
async def on_guild_update(before, after):
    session = requests.Session()
    guild = after
    if after.vanity_url_code != before.vanity_url_code:
        logging.info(f"The Vanity `{before.vanity_url_code}` was dropped")
            
        if guild.id in guild_idss:    
            code = {"code": before.vanity_url_code}
            base = f"https://discord.com/api/v9/guilds/{guild.id}/vanity-url"
            r = session.patch(url=base, headers={"Authorization": tok}, json=code)
            if r.status_code == 200:
                logging.info(f"Vanity `{before.vanity_url_code}` was protected")
                
            else:
                logging.info(f"Error Occured Protecting vanity | {r.status_code} | {r.json()}")
                    

            
client.run(TOKEN)