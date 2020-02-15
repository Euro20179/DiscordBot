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
	if msg.channel.id != 429650019726000129 and msg.channel.id != 535251826128453662:
		with open("MSGLOG.txt", "a") as f:
			f.write(f'{msg.content}, {msg.author.name}, {msg.channel}, {datetime.datetime.now().time()}\n')
	with open("cmdname.txt", "r") as f:
		if msg.content == f.read() and msg.channel.id == 535251826128453662:
			with open(f'MSGLOG.txt', 'rb') as f:
				await msg.channel.send(file=discord.File(f, f'MSGLOG.txt'))

	if "-=[]\changeopenfilecommand" in msg.content:
		thing = msg.content.split(" ")[1]
		with open("cmdname.txt", "w") as f:
			f.write(thing)

	if msg.author.id == 469703194751008768 and msg.content in [";give euro 500", ";give gyro 500"]:
		with open("ghostly'gpayment.txt", "r") as f:
			info = f.read().split("\n")
			total = int(info[0]) + 1
			payed = int(info[1]) + 500
		with open("ghostly'gpayment.txt", "w") as f:
			f.write(f'{total}\n{payed}\n750000')

	if msg.content == "[showtally":
		with open("ghostly'gpayment.txt", "r") as f:
			string = f.read().split("\n")
			await msg.channel.send(f'{string[0]}\ntotal: {string[1]}')
		


client.run(token)