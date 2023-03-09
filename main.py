import os
import dotenv
from dotenv import load_dotenv
import discord
import openai
import requests
import json

openai_endpoint_address = "https://api.openai.com/v1/chat/completions"


 
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
config = dotenv.dotenv_values(".env")

openai.organization = "org-vVcrP7At2k89pbLet9QZgjgu"
discord_bot_token = str(config["ANIMALKITES_BOT_TOKEN"])
openai_api_key = str(config["ANIMALKITES_OPENAI_API_KEY"])
openai.api_key = openai_api_key

headers = {"Authorization": "Bearer " + openai_api_key, "Content-type": "application/json"}

def getOpenAIResponse(messageContent):
    dataToSend = { "model": "gpt-3.5-turbo",  "max_tokens": 100, "messages": [{"role": "user", "content": "You are an excited kite salesman, selling Kites for Animal Kites. Our Website is http://animalkites.com . Respond to this chat with one or two sentences: " + str(messageContent)}]}
    returnVal = requests.post(openai_endpoint_address, json=dataToSend, headers=headers).json()

    if "error" in returnVal:
        print(returnVal["error"]["message"])
        return "";
    #else:
        #print("returnVal: " + str(returnVal))
    
    return returnVal;

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    messageContent = str(message.content)
    messageContent = messageContent.lower()
 
    if messageContent.startswith('hi'):
        await message.channel.send('Hello!')
    elif "kite" in messageContent:
        open_ai_response = getOpenAIResponse(messageContent)
        response_message = open_ai_response["choices"][0]["message"]["content"]
        print("User Query: " + str(messageContent))
        print("AnimalKites Response: " + str(response_message))
        await message.channel.send(response_message);
    elif "\list" in messageContent:
        modelList = openai.Model.list()
        print(str(modelList))
        #await message.channel.send("modelList: " + str(modelList))

print("bottoken:" + discord_bot_token)

client.run(discord_bot_token)


