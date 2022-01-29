import discord
import os
import requests
import json
import random
from nanoid import generate
from dotenv import load_dotenv

load_dotenv()

#Creates a conection to Discord
client = discord.Client();

greetings = [ "hello", "hi", "hey", "help", "support", "good morning", "good evening", "assistance"]

issues = [ "bad quality", "not the same as in the photo", "too large", "too loose", "doesn't fit", "incorrect size", "wrong", "issue"]

solutions = [ "You can exchange the value of the item for in-app credits", "You can change the item for another one", "You can get a refund\n"]

#Gets response from the api that you choose
#Return arrays of greetings to respond to the user
def get_greetings():
  response = requests.get("http://127.0.0.1:3000/greetings")
  greetings = json.loads(response.text)
  return (greetings)

#Returns array of apology phrases
def get_apologies():
    response = requests.get("http://127.0.0.1:3000/apology")
    apologies = json.loads(response.text)
    return (apologies)

def get_solutions():
    response = requests.get("http://127.0.0.1:3000/solutions")
    solutions = json.loads(response.text)
    return (solutions)

def post_ticket(requestMessage):
    id = generate()
    requests.post('http://127.0.0.1:3000/ticket', data = {'message': requestMessage, 'id': id})
    return id

#Register a new event
@client.event
async def on_ready(): #Event will be called when the event is ready to be used
  print("Chatbot up and running!")

@client.event
async def on_message(message):
  #If the last message sent was from the bot itself, don't do anything
  if message.author == client.user:
    return

  msg = message.content.lower()
  solutions = False

  #if the last message starts with the following keyword, respond
  #if msg.startswith(':one:'): DOESNT WORK
  #  await message.channel.send("hello")

  if any(word in msg for word in greetings):
      greeting_responses = get_greetings()
      await message.channel.send(random.choice(greeting_responses)['message'])

  if any(word in msg for word in issues):
      solutions = True
      apology_responses = get_apologies()
      await message.channel.send(random.choice(apology_responses)['message'])

  if solutions:
      await message.channel.send('React to this message to provide you with all available solutions 😎')

  if message.content == "1️⃣":
    #send post request
    ticketId = post_ticket('Exchange the value of the item for in-app credits.')
    finalMessage = 'Your ticket has been successfully created. This is your request id for future reference: ' + ticketId
    await message.channel.send(finalMessage)
  elif message.content == "2️⃣":
    #send post request
    ticketId = post_ticket('Get refund')
    finalMessage = 'Your ticket has been successfully created. This is your request id for future reference: ' + ticketId
    await message.channel.send(finalMessage)
  elif message.content == "3️⃣":
    #send post request
    ticketId = post_ticket('Change the item for another one')
    finalMessage = 'Your ticket has been successfully created. This is your request id for future reference: ' + ticketId
    await message.channel.send(finalMessage)


@client.event
async def on_reaction_add(reaction, user):
    option = 0
    #If the message being reacted is the bot's
    if reaction.message.author == client.user:
        await reaction.message.reply('These are all our available solutions!')
        solution_responses = get_solutions()
        i = 0
        reply = ''
        for solution in solution_responses:
            i += 1
            reply += str(i) + '. ' + solution['message'] + '\n'
        await reaction.message.reply(reply + 'Typeone of the following emojis depending on what you want to choose: :one:, :two:, :three:')

#token = os.environ['DISCORD_TOKEN']
token = os.getenv('DISCORD_TOKEN')
client.run(token)