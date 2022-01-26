import os
import discord
import requests
import random
from replit import db


client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "depressing"]

stock_encouragements = [
  "Cheer up!",
  "Hang in there champ!",
  "You are a great person / bot :) ",
  "The team is always here for you",
]

def update_encouragements(message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > int(index):
    del encouragements[int(index)]
  db["encouragements"] = encouragements

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = response.json()
  quote = (json_data[0]['q']) + " -" + (json_data[0]['a'])
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith("$hello"):
    await message.channel.send("Well hi!")
  
  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)
  
  options = stock_encouragements
  if "encouragements" in db.keys():
    dbList = list(db["encouragements"])
    options = options + dbList
  
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
  
  if msg.startswith("$newe"):
    newMessage = msg.split("$newe ",1)[1]
    update_encouragements(newMessage)
    await message.channel.send("New encouragement added. Thanks for the help!")

  if msg.startswith("$dele"):
    encouragements = []
    if "encouragements" in db.keys():
      index = msg.split("$dele ", 1)[1]
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

client.run(os.getenv("TOKEN"))