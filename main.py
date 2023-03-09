import os
import dotenv
from dotenv import load_dotenv
import discord
import openai
import requests
import json
import random
import string

openai_endpoint_address = "https://api.openai.com/v1/chat/completions"
openai_imageGeneration_address = "https://api.openai.com/v1/images/generations"




 
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
config = dotenv.dotenv_values(".env")

openai.organization = "org-vVcrP7At2k89pbLet9QZgjgu"
discord_bot_token = str(config["ANIMALKITES_BOT_TOKEN"])
openai_api_key = str(config["ANIMALKITES_OPENAI_API_KEY"])
openai.api_key = openai_api_key

num_generations = 0



def generateImageFromPrompt(prompt):
    headers = {"Authorization": "Bearer " + openai_api_key, "Content-type": "application/json"}
    dataToSend = { "prompt": prompt, "n": 1, "size": "512x512" }
    returnVal = requests.post(openai_imageGeneration_address, json=dataToSend, headers=headers).json()
    returnData = returnVal["data"]
    returnUrls = []

    for record in returnData:
        url = record["url"]
        returnUrls.append(url)

    return returnUrls


def getOpenAIResponse(messageContent):
    headers = {"Authorization": "Bearer " + openai_api_key, "Content-type": "application/json"}
    dataToSend = { "model": "gpt-3.5-turbo",  "max_tokens": 100, "messages": [{"role": "user", "content": "You are an excited kite salesman, selling Kites for Animal Kites. Our Website is http://animalkites.com . Respond to this chat with one or two sentences: " + str(messageContent)}]}
    returnVal = requests.post(openai_endpoint_address, json=dataToSend, headers=headers).json()

    if "error" in returnVal:
        print(returnVal["error"]["message"])
        return "";
    #else:
        #print("returnVal: " + str(returnVal))
    
    return returnVal;

def generateImageName():
    imageName = ''.join(random.choices(string.ascii_uppercase, k=5)) + ".png"
    return imageName

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    num_generations = 0
 
@client.event
async def on_message(message):
    global num_generations
    if message.author == client.user:
        return

    messageContent = str(message.content)
    messageContent = messageContent.lower()
 
    if messageContent.startswith('hi'):
        await message.channel.send('Hello!')
    elif "kite" in messageContent:
        open_ai_response = getOpenAIResponse(messageContent)
        response_message = open_ai_response["choices"][0]["message"]["content"]
        await message.channel.send(response_message)
        
        # only generate an image every 10 times.
        if num_generations % 10 == 0:
            await message.channel.send("\n Hang on I'll show you an image....")
            generatedImageURLs = generateImageFromPrompt(str(response_message))
        
            i = 0

            # Loop through urls, saving each picture
            for imageURL in generatedImageURLs:
                if i == 0:
                    # Get the image
                    img_data = requests.get(imageURL).content

                    # Create a random name for this image.
                    newImageName = generateImageName()

                    # Save the image to the file system
                    with open("images/" + newImageName, 'wb') as handler:
                        handler.write(img_data)

                

                    await message.channel.send(file=discord.File("images/" + newImageName))
                i = i + 1

        print("User Query: " + str(messageContent))
        print("AnimalKites Response: " + str(response_message))
        num_generations = num_generations + 1
        
    elif "\list" in messageContent:
        modelList = openai.Model.list()
        print(str(modelList))
        #await message.channel.send("modelList: " + str(modelList))

print("bottoken:" + discord_bot_token)

client.run(discord_bot_token)


