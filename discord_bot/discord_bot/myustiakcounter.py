import discord
from discord.ext import commands
import time, datetime
import threading

token = "NjY5NzQ2NjQwNTE2ODA4NzA0.XjDUbg.MSR25egyVRNDTcutN5y9k7-DGSU"

client = commands.Bot(command_prefix="=")

@client.event
async def on_ready():
	print("MESSAGES BEING DELETED")

@client.event
async def on_message(msg):
	if msg.author.id == 311621977339068418 and msg.channel.id != 658815060646297659:
		await msg.delete()
		print("message deleted")




client.run(token)