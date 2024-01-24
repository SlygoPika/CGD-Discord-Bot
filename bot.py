from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands

class Bot:
    def __init__(self):
        load_dotenv()
        self.TOKEN: Final[str] = os.getenv('BOT_TOKEN')
        self.intents: Intents = Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        self.intents.reactions = True
        self.client: Client = Client(intents=self.intents)
        self.bot = commands.Bot(command_prefix='$', intents=self.intents, help_command=None)


bot = Bot()
