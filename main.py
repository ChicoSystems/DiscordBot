import os
from dotenv import load_dotenv
import discord
 
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
bot_token = str(os.getenv("ANIMALKITES_BOT_TOKEN"))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
 
    if message.content.startswith('hi'):
        await message.channel.send('Hello!')

print("bottoken:" + bot_token)

client.run(bot_token)
