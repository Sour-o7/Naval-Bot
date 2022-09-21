from __future__ import print_function
from discord.ext import commands
import discord
import os.path
import os
import threading

#Naval Version 2.0.0
#9/20/2022

client = commands.Bot(command_prefix="++", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Online")
    
    # Load cogs
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await client.load_extension("cogs." + f[:-3])
client.run('TOKEN')