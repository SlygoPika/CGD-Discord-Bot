from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message

load_dotenv()
TOKEN: Final[str] = os.getenv('BOT_TOKEN')
print(TOKEN)

# This example requires the 'message_content' intent.

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    # response: str = get_response(message.content)
    # await message.channel.send(response)
    if not user_message:
        print('No message. Intents were not enabled properly.')
        return
    
    await message.channel.send('Hello World')

client.run(TOKEN)