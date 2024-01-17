from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
from bot import Bot, bot
import asyncio

from cogs.greetings import Greetings

@bot.client.event
async def on_message(message):
    if message.author == bot.client.user:
        return
    
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot.bot:
        await load_extensions()
        await bot.bot.start(bot.TOKEN)

asyncio.run(main())

#bot.run()
