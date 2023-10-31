# This example requires the 'message_content' intent.
import discord
from discord.ext import commands
import requests
import os
from datetime import datetime
import os
import openai

MY_SECRET = os.getenv("SECRET_KEY")
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('/trick'):
    prompt = message.content[7:]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant."
        }, {
            "role":
            "user",
            "content":
            f"You are a master of halloween. You will answer to any question in a halloween tone and halloween emojis. No matter it make sense or not, but it must be funny and reminds about halloween. You actually perform trick and ask for treat from user. Also try to keep it short and easy. Here is the input\n {prompt}"
        }])
    await message.channel.send(response["choices"][0]["message"]["content"])

  elif message.content.startswith('/treat'):
    prompt = message.content[7:]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant."
        }, {
            "role":
            "user",
            "content":
            f"You are a master of halloween. User gave you treats for your awesome tricks. As an appreciation, you write the given input name in bold, stylish, decorated with emojis so that user get impressed. At the end of the emoji name, write one line about this treat. Here is the input name\n {prompt}"
        }])
    await message.channel.send(response["choices"][0]["message"]["content"])
  # elif "bot" or "hello" or "gm" in message.content:
  else:
    await message.channel.send(
        '👻🕸️🍭I am a HALLOWEEN exclusive bot. Write **/trick<space><ask-a-question or anything>** to get tricked or **/treat<space><your-name>** to give treat to bot.🧙‍♂️🔮🎃'
    )


client.run(MY_SECRET)
