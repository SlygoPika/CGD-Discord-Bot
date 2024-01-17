import discord
import dotenv


TOKEN = dotenv.get_key(".env", "BOT_TOKEN")
print(TOKEN)

# This example requires the 'message_content' intent.


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

# keep_alive()
client.run(TOKEN)
