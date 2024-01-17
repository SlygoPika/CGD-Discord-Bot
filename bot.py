from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands

# # COG IMPORTS
# from src.commands import ChannelInit
from cogs.greetings import Greetings


# Bot class
# Members:
#   TOKEN: Final[str]
#   intents: Intents
#   client: Client
#   bot: commands.Bot
class Bot:
    def __init__(self):
        load_dotenv()
        self.TOKEN: Final[str] = os.getenv('BOT_TOKEN')
        self.intents: Intents = Intents.default()
        self.intents.message_content = True
        self.client: Client = Client(intents=self.intents)
        self.bot = commands.Bot(command_prefix='$', intents=self.intents)
    
bot = Bot()
