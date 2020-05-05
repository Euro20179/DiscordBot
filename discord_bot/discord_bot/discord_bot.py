import discord
from discord.ext import commands
import time, datetime
import random
import string
import pyautogui
import wikipedia

Stop = False

def stopp():
	global Stop
	Stop = False if Stop else True

def delTrue(msg):
	if msg.lower() not in ["false", "f", "n", "no"]: return True
	else: return False

token = "NjQxNzk1NjU2Mzc3MTcyMDAw.XcNk8g.HEvnaXjuXFQhN1iilaaffbiPcoo"

client = commands.Bot(command_prefix="[")

def logCMD(cmd):
	t = datetime.datetime.now().time()
	print(cmd, t)
	with open("LOG.txt", "a") as f:
		f.write(f'{cmd}, {t}\n')


@client.event
async def on_ready():
	print("ONLINE")

@client.command()
async def ping(ctx, delete="false"):
	"""
	<delete t/f>
	"""
	if delTrue(delete): await ctx.message.delete()
	await ctx.send(f':ping_pong: {round(client.latency * 1000)}ms')	
	logCMD(f"Ping, {ctx.message.author}")

@client.command(aliases=['8ball', 'luckmachine'])
async def magicball(ctx, *question, delete="false"):
	question = " ".join(question)
	if "delete=" in question:
		question = question.split("delete=")
		if delTrue(question[1]): await ctx.message.delete()
		question = question[0]
	with open("mballresonse.txt", "r") as f:
		responses = f.read().split("\n")

	await ctx.send(f'Answer: {random.choice(responses)}')
	logCMD(f"magicball, {ctx.message.author}")

@client.command()
async def spam(ctx, messages, *message, delete="false"):
	"""
	(amount) (count (y/n)) (message) add delete=t to delete the message you sent
	"""

	count = 0
	if int(messages) > random.randint(30000, 100000):
		await ctx.send("pls consult a psychiatrist that's too many messages")
	message = ' '.join(message)
	if "delete=" in message:
		message = message.split("delete=")
		if delTrue(message[1]):
			await ctx.message.delete()
		message = message[0]
	if message == "done":
		await ctx.send(random.choice(["HAHA NICE TRY FOOLING EVERYONE WITH THE DONE", "nope can't say that", "you cannot say 'done'"]))
		return
	logCMD(f"spam, {messages}, {message} {ctx.message.author}")
	try: int(messages)
	except: 
		await ctx.send("not a valid number of messages")
		return
	for x in range(int(messages)):
		if Stop:
			stopp()
			break
		count += 1
		await ctx.send(message)
		print(f"{count}/{messages} {message}")
		time.sleep(random.uniform(.1, 1.3))
	if random.random() > .99:
		await ctx.send("You found an easter egg hehe")
	else:
		await ctx.send(random.choice(["done", "Done"]))
	

@client.command()
async def randomface(ctx, delete="false"):
	"""
	<delete t/f>
	"""
	if delTrue(delete): await ctx.message.delete()
	await ctx.message.delete()
	eyes = [":", ";"]
	mouths = [")", "(", "{", "}", "[", "]", "p", "P", "d", "l"]
	await ctx.send(f'{random.choice(eyes)}{random.choice(mouths)}')
	logCMD(f"random face, {ctx.message.author}")

@client.command()
async def thetroycommand(ctx, delete="false"):
	"""
	the troy command :)
	<delete t/f>
	"""
	if delTrue(delete): await ctx.message.delete()
	await ctx.send(random.choice(["meow", "7", "**7**", "*7*", "i love waluigi"]))
	logCMD(f"thetroycommand, {ctx.message.author}")
@client.command()
async def leorty(ctx, seconds=2, delete="false"):
	"""
	[time] <delete t/f>
	"""
	try:
		float(seconds)
	except:
		await ctx.send("Not a valid number of seconds")
		return
	if delTrue(delete):
		ctx.message.delete()
	logCMD(f"leorty, {seconds} {ctx.message.author}")
	start = time.time()
	while time.time() - start <= float(seconds):
		if Stop:
			stopp()
			break
		for x in "leorty":
			await ctx.send(x)

@client.command()
async def mymoney(ctx):
	"""
	useless
	"""
	logCMD(f"mymoney, {ctx.message.author}")
	localUser = ctx.message.author
	await ctx.send(f'{localUser} you have ${random.randint(0, 1000000)}')

@client.command()
async def alphabet(ctx, delete="false"):
	"""
	says the alphabet <delete t/f>
	"""
	if delTrue(delete): await ctx.message.delete()

	logCMD(f"alphabet, {ctx.message.author}")
	if random.random() > .98: await ctx.send("zyxwvutsrqponmlkjihgfedcba")
	else: await ctx.send("abcdefghijklmnopqrstuvwxyz")
	

@client.command()
async def unicodechar(ctx, amount=1, delete="t"):
	"""
	[amount] <delete t/f>
	"""
	if delTrue(delete):
		await ctx.message.delete()
	try:
		int(amount)
	except:
		await ctx.send("Not a valid number")
		return

	logCMD(f"unicodechar, {amount} {ctx.message.author}")
	for x in range(amount):
		if Stop:
			break
		char = random.randint(0, 185000)
		await ctx.send(f'{chr(char)} value: ({char})')
		time.sleep(random.uniform(.2, .9))

@client.command()
async def serveremote(ctx, amount=1, delete="t"):
	"""
	[amount] <delete t/f>
	"""
	try:
		int(amount)
	except:
		await ctx.send("Not a valid number")
		return
	if delTrue(delete):
		await ctx.message.delete()
	logCMD(f"serveremote, {amount} {ctx.message.author}")
	emotes = client.emojis
	for x in range(amount):
		await ctx.send(f'{random.choice(emotes)}')

@client.command()
async def doesnothing(ctx, *filename):
	filename = " ".join(filename)
	logCMD(f"doesnothing, {filename} {ctx.message.author}")
	with open(f".\\roles\\{filename}.txt", "w") as f:
		unwn = 0
		for x in client.get_all_members():
			try:
				f.write("\n")
				f.write(str(x))
			except:
				f.write(f"UNWRITEABLE{unwn}")
				unwn += 1
			for y in x.roles:
				if "HAPPY" in y.name:
					f.write("HAPPY BIRTHDAY")
				elif "Cart Surfer Queen" in y.name:
					f.write("CS Queen")
				elif "Cart Surfer King" in y.name:
					f.write("CS King")
				elif "Flower Lover" in y.name:
					f.write("Flower lover")
				elif "Rain Lover" in y.name:
					f.write("Rain Lover")
				else:
					try:
						f.write(y.name + "\n")
					except: f.write("UNICODE\n")


@client.command()
async def spacer(ctx, spaces, *word):
	"""
	[spacer [spaces] word
	"""
	try: int(spaces)
	except:
		await ctx.send("Not a valid number of spaces")
		return
	word = " ".join(word)
	logCMD(f"spacer, {spaces}, {word} {ctx.message.author}")
	await ctx.message.delete()
	spaces = int(spaces)
	add = ""
	for x in range(spaces):
		if Stop:
			stopp()
			break
		add += " "
	word = add.join(word)
	await ctx.send(word)

@client.command()
async def thelevicommand(ctx, delete="false"):
	"""
	the levi command :) <delete t/f>
	"""
	if delTrue(delete): ctx.message.delete()

	logCMD(f"thelevicommand, {ctx.message.author}")
	await ctx.send(random.choice(["", "catssssss", "pokemonnnnn", "i'm bored", "i'm gonna go bye", "i have bored", "i need infinite money"]))

@client.command()
async def currentversion(ctx, delete="false"):
	"""
	the current version <delete t/f>
	"""
	if delTrue(delete): ctx.message.delete()
	logCMD(f"currentversion, {ctx.message.author}")
	await ctx.send("B_1.4.2")

@client.command()
async def upperlower(ctx, *phrase):

	"""
	[words]
	"""
	await ctx.message.delete()
	phrase = (" ".join(phrase)).lower()

	logCMD(f"upperlower, {phrase} {ctx.message.author}")

	newPhrase = []

	for val, letter in enumerate(phrase):
		if val > 0:
			if phrase[val - 1] != " " and newPhrase[val - 1].islower():
				letter = letter.upper()
			elif newPhrase[val - 2].islower() and phrase[val - 1] == " ":
				letter = letter.upper()
		newPhrase.append(letter)

	await ctx.send("".join(newPhrase))
	print("".join(newPhrase))

@client.command()
async def longmessage(ctx, delete="false"):
	"""
	<delete t/f>
	"""
	if delTrue(delete): await ctx.message.delete()
	await ctx.send("```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````hI```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
	logCMD(f"longmessage, {ctx.message.author}")

@client.command()
async def clear(ctx, amount=10):
	try: int(amount)
	except:
		await ctx.send("Not a vlid number")
		return
	await ctx.channel.purge(limit=amount)
	logCMD(f"clear, {amount} {ctx.message.author}")


@client.command()
async def flush(ctx, *user):
	"""
	include delete=t at the end of the message to delete your command message
	"""
	user = " ".join(user)
	if "delete=" in user:
		user = user.split("delete=")
		if user[1] in ["true", "t"]:
			await ctx.message.delete()
		user = user[0]
	await ctx.send(user + " has been flushed down the toilet :toilet::toilet::toilet::toilet::toilet::toilet::toilet::toilet:")
	logCMD(f"flush, {user} {ctx.message.author}")

@client.command()
async def stop(ctx, delete="false"):
	if delTrue(delete):
		ctx.message.delete()
	stopp()
	logCMD(f"STOPPED, {ctx.message.author}")

@client.command()
async def complexmessage(ctx, send, filename, *message):
	"""
	usage: [message yes/no "filename in these quotes (must end with .txt or a file extention)" what to put in the file in these quotes" if you want to use quotes in the message use single quotes ex: [message "hi.txt" "he said, 'ok'"
	"""
	send = send.lower()
	falses = ["f", "false", "no", "n"]
	dms = ["d", "dm", "pm", "p"]
	if send in falses: send = False
	elif send in dms: dm = True; send = False
	else: dm = False; send = True
	await ctx.message.delete()
	message = " ".join(message)
	logCMD(f"complexmessage, {filename}, {message} {ctx.message.author}")
	with open(f'.\\message\\{filename}', "w") as f:
		f.write(message)
	if send:
		with open(f'.\\message\\{filename}', 'rb') as f:
			await ctx.send(file=discord.File(f, f'{filename}'))
	if dm:
		with open(f'.\\message\\{filename}', 'rb') as f:
			await ctx.author.send(file=discord.File(f, f'{filename}'))

@client.command()
async def message(ctx, send, filename, *message):
	"""
	usage: [message yes/no/dm "filename" message
	"""
	send = send.lower()
	falses = ["f", "false", "no", "n"]
	dms = ["d", "dm", "pm", "p"]
	if send in falses: send = False
	elif send in dms: dm = True; send = False
	else: dm = False; send = True
	await ctx.message.delete()
	message = " ".join(message)

	discord.ChannelType.private

	logCMD(f"message, {filename}, {message} {ctx.message.author}")
	with open(f'.\\message\\{filename}.txt', "w") as f:
		f.write(message)
	if send:
		with open(f'.\\message\\{filename}.txt', 'rb') as f:
			await ctx.send(file=discord.File(f, f'{filename}.txt'))
	if dm:
		with open(f'.\\message\\{filename}.txt', 'rb') as f:
			await ctx.author.send(file=discord.File(f, f'{filename}.txt'))
@client.command()
async def echo(ctx, *msg):
	await ctx.message.delete()
	msg = " ".join(msg)
	if random.random() > .98: await ctx.author.send("the secret message dm euro for a doubley secret role, if you tell anyone how you got this the role will be taken away\nif you already have the role, you may choose to dm a screenshot of this message to someone, and they have the chance to get the role")
	await ctx.send(msg)
	logCMD(f"echo, {msg} {ctx.message.author}")


@client.command()
async def sanity(ctx, *obj, delete="false"):
	
	obj = " ".join(obj)
	if "delete=" in obj:
		obj = obj.split("delete=")
		if delTrue(obj[1]):
			await ctx.message.delete()
		obj = obj[0]
	san = random.uniform(-1, 101)
	logCMD(f'sanity, {obj} {san} {ctx.message.author}')
	if san > 100:
		await ctx.send(f'{obj} is so sane that they have become the universe itself')
	elif san < 0:
		await ctx.send(f'how is {obj} even alive')
	else:
		await ctx.send(f'{obj} has {san}% sanity')

@client.command()
async def coin(ctx, delete="false"):
	"""
	<delete t/f>
	"""
	if delTrue(delete): await ctx.message.delete()
	res = "heads" if random.random() >= .5 else "tails"
	await ctx.send(res)
	logCMD(f'coin, {res} {ctx.message.author}')

@client.command()
async def rand(ctx, low=1, high=10, delete="false"):
	"""
	low number, high number
	ex: [rand 1 100 <delete t/f>
	"""
	if delTrue(delete): await ctx.message.delete()

	if low >= high:
		await ctx.send("Low must be lower than high")
		return
		logCMD(f'rand, ERROR, {ctx.message.author}')
	res = random.randint(int(low), int(high))
	await ctx.send(res)
	logCMD(f'rand, {res} {ctx.message.author}')

@client.command()
async def freerole(ctx, delete="false"):
	"""
	<delete t/f>
	"""
	if delTrue(delete): await ctx.message.delete()
	if random.random() > .98:
		ctx.author.send("dm euro for a free role but if you tell anyone how to get it it will be taken away\nif you already have the role, you may choose to dm a screenshot of this message to someone, and they have the chance to get the role")
	await ctx.send("did you really think this would give you a free role")

@client.command()
async def rolecount(ctx, user : discord.Member, delete="false"):
	"""
	rolecount of a user
	[rolecount @person <delete t/f>
	"""
	if delTrue(delete):
		ctx.message.delete()
	roleCount = -1
	for x in user.roles:
		roleCount += 1
	await ctx.send(roleCount)
	logCMD(f'rolecount, {user}: {roleCount} {ctx.message.author}')

@client.command()
async def mrolecount(ctx):
	"""
	your role count
	"""
	roleCount = -1
	for x in ctx.author.roles:
		roleCount += 1
	await ctx.send(roleCount)
	logCMD(f'rolecount, {user}: {roleCount} {ctx.message.author}')

@client.command()
async def family(ctx):
	logCMD(f'family, {ctx.message.author}')
	with open("family.txt", "r") as f:
		await ctx.send(f.read())
	
@client.command()
async def mballreply(ctx, *msg):
	msg = " ".join(msg)
	logCMD(f"mballreply, {msg}, {ctx.message.author}")
	with open("mballresonse.txt", "a") as f:
		f.write(msg + "\n")
	await ctx.send("message added")

@client.event
async def on_voice_state_update(member, before, after):
	if not  before.channel and after.channel:
		role = discord.utils.get(member.guild.roles, name="vc")
		await member.add_roles(role)
	elif before.channel and not after.channel:
		role = discord.utils.get(member.guild.roles, name="vc")
		await member.remove_roles(role)

client.run(token)