from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands

load_dotenv()
TOKEN: Final[str] = os.getenv('BOT_TOKEN')

# This example requires the 'message_content' intent.

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

bot = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return


client.run(TOKEN)
