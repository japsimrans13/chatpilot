import discord
import os

#Creates a conection to Discord
client = discord.Client();

#Register a new event
@client.event
async def on_ready(): #Event will be called when the event is ready to be used
  print("Chatbot up and running!")

discordToken = os.environ['discordToken']
client.run(discordToken);