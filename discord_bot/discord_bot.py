import discord
from discord.ext import commands
import time, datetime
import random
import string
import asyncio
import json
import tracemalloc
import requests
import bs4 as bs

#TODO Make a stopwatch and a timer

#TODO make countries hangman
#TODO flag trivia
#TODO LITERALLY ANYTHING WITH COUNTRIES

tracemalloc.start()

DELETE = "--delete"
VERSION = "3.5.3"
Stop = False

playingGuessingGame = {}
runningStopwatch = {}
reacting = {}
playingHangman = {}

PREFIX = "[]"

token = "NjQxNzk1NjU2Mzc3MTcyMDAw.XcNk8g.HEvnaXjuXFQhN1iilaaffbiPcoo"

client = commands.Bot(command_prefix=PREFIX)

mballresponseFilePath = "../mballresponse.txt"
levelingDataFilePath = "../levelingData.json"
commandusageFilePath = "../commandusage.json"

BASICINFO = {"level": 1, "xp": 0, "required": 1000, "lastTalked": 0, "message": '{author} you have leveled up to level {level}, very cool'}

def isBot(msg, client)->bool:
	if msg.author == client.user or msg.author.bot: return True
	return False

async def formatDateTime(createdAt : datetime.datetime)->str:
	return f'{createdAt.month}/{createdAt.day}/{createdAt.year} at {createdAt.hour}:{createdAt.minute}:{createdAt.second}'

async def getUserInContent(msg : discord.Message, c : str, cmd : str)->discord.User:
	c = str(c.split(cmd)[1].strip())
	c = c[3:-1] if "<@!" in c else c
	if not c: c = str(msg.author.id)
	user = findMember(c, msg)
	user = msg.author if not user else user
	return user

async def giveXP(msg : discord.Message)->None:
	if isBot(msg, client): return
	with open(levelingDataFilePath, "r+") as f:
		data = json.load(f)
		if (userInfo := data.get(str(msg.author.id))):
			lastTalked = int(userInfo["lastTalked"])
			if time.time() - lastTalked >= 60:
				level = userInfo["level"]
				xp = userInfo["xp"]
				xp += random.randint(15, 100)
				lastTalked = time.time()
				required = userInfo["required"]
				levelUpMessage = userInfo.get("message")
				if not levelUpMessage: rawLvlMsg = '{author} you have leveled up to level {level}, very cool'
				else: rawLvlMsg = levelUpMessage
				if xp >= required:				
					level += 1
					if levelUpMessage: levelUpMessage = levelUpMessage.replace("{author}", msg.author.mention).replace("{level}", str(level)).replace("{time}", await formatDateTime(datetime.datetime.now())).replace("{emote}", str(random.choice(client.emojis))).replace("{channel}", msg.channel.name)
					else: levelUpMessage = f'{msg.author.mention} you have leveled up to level {level}, very cool'
					xp //= 2
					required = round((1000 * level) * 1.1)
					userInfo = {"level": level, "xp": xp, "required": required, "lastTalked": lastTalked, "message": rawLvlMsg}
					if levelUpMessage not in ["none", "None", "null", "Null"]:
						await msg.channel.send(levelUpMessage)
				required = round((1000 * level) * 1.1)
				userInfo = {"level": level, "xp": xp, "required": required, "lastTalked": lastTalked, "message": rawLvlMsg}
			data[str(msg.author.id)] = userInfo
		else:
			data[str(msg.author.id)] = BASICINFO
			data[str(msg.author.id)]["lastTalked"] = time.time()
		clearFile(f)
		json.dump(data, f)

async def reduceXP(msg : discord.Message)->None:
	if isBot(msg, client): return
	with open(levelingDataFilePath, "r+") as f:
		data = json.load(f)
		for user in data.keys():
			if time.time() - data[user]["lastTalked"] >= 86400:
				if data[user]["xp"] > 0:
					data[user]["xp"] -= random.randint(0, 1)
				if data[user]["xp"] <= (data[user]["level"] * 1000) // 2 and data[user]["level"] > 0:
					data[user]["level"] -= 1
					data[user]["xp"] = (data[user]["level"] * 1000) // 2 + 1500
		clearFile(f)
		json.dump(data, f)

def testInContent(content : str, *testfor)->str:
	for x in testfor:
		if x.lower() in content.lower():
			return x
	return ""

def TICDelete(content : str)->bool:
	return DELETE in content

def getCmd(content : str)->str:
	return content.split(" ")[0][1:]				

def splitContent(content : str, *split, index=None, func=None)->str:
	for x in split:
		if x in content:
			ret = content.split(x)
			if func and index:
				ret = func(content.split(x)[index])
			elif func: ret = func(x)
			elif index: ret = content.split(x)[index]
			return ret
	return ""

def check_int(s)->bool:
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def stop(*args, **kwargs)->None:
	global Stop
	Stop = False
	if args: return random.choice(args)

def userHasRole(msg : discord.Message, *roles)->bool:
	return True if discord.utils.find(lambda r: r.name in roles, msg.author.roles) else False

def isInt(testee : str)->bool:
	try: 
		int(testee)
		return True
	except:	return False

def findMember(c : str, msg : discord.Message)->discord.Member:
	return discord.utils.find(lambda m: str(m.id) == c or str(m.display_name.split("#")[0].lower()) == c.lower(), msg.guild.members)

def clearFile(f)->None:
	f.seek(0)
	f.truncate()

async def oneLineCmd(msg : discord.Message, say : str, delete=True)->discord.Message:
	if TICDelete(msg.content) and delete: 
		say = say.replace(DELETE, "")
		await msg.delete()
	msg = await msg.channel.send(say)
	return msg

async def hlp(msg, content, cmd="help"):
	cat = splitContent(content, cmd + " ", index=1).upper()
	with open("cmds.json", "r") as j:
		data = json.load(j)
		if cat in [c for c in data.keys()] + [""]:
			if not cat:
				embed = discord.Embed(title="Help", color=discord.Color(0x00ffe2))
				for category in data.keys():
					embed.add_field(name=category, value=data[category].get("desc"))
			else:
				embed = discord.Embed(title=cat, color=discord.Color(0x00ffe2))
				for command in data[cat].keys():
					if command == "desc": continue
					embed.add_field(name=command, value=f'``{command}`` {data[cat][command]["params"]}', inline=False)
			await msg.channel.send(embed=embed)
			return

	with open("cmds.json", "rb") as j:
		if testInContent(content, "--all", "--indepth"):
			await msg.channel.send(file=discord.File(j, "cmds.json"))
		else:
			data = json.load(j)
			command = splitContent(content, " ", index=1)
			embed = discord.Embed(title=command, color=discord.Color(0x00ffe2))
			for cat in data.values():
				if cat == "desc": continue
				if (cmmd := cat.get(command)):
					params = cmmd["params"]
					desc = cmmd["desc"]
					aliases = cmmd.get("aliases")
					text = f'{command} {params}\n{desc}\n\nALIASES: {aliases}'
					break
			embed.add_field(name="description", value=text)
			await msg.channel.send(embed=embed)

async def spam(msg, messages, message, BlockStop=False):
	global Stop
	for _ in range(int(messages)):
		if Stop and not BlockStop:
			await msg.channel.send(stop("stopped spam", "Stopped spam"))
			return ""
		msg = await msg.channel.send(random.choice(message))
		await asyncio.sleep(random.uniform(.6, 1.3))
	return msg

async def ping(msg, content, cmd="ping"):
	if TICDelete(content): await msg.delete()

	if "<@" in content:
		msg = await msg.channel.send("are you trying to ping someone..... don't do that. :/")
		
	if random.random() >= .95:
		await msg.author.send("upupdowndownleftrightleftright")
		await asyncio.sleep(5)
		await msg.author.send("OH SHOOT I WASNT SUPPOSED TO SAY TH-")
		await asyncio.sleep(1)
		await msg.author.send("goodbye")

	if random.random() >= .99:
		msg = await msg.channel.send("uh yeah tbh i don't really know what this does, like i have an idea but like idk")
	elif random.random() >= .97:
		msg = await msg.channel.send("LOL GET PRANKD THIS DOES NOTHING ROFL XD XD XD XD XD")
	else: msg = await msg.channel.send(f':ping_pong: {round(client.latency * 1000)}ms')	
	return msg

async def echo(msg, content, cmd="echo"):
	content = content[len(cmd) + 2:]
	if not TICDelete(content): 
		await msg.delete()
		content = content.replace(DELETE, "")
	if "--e" in content:
		c = content.replace(" --e", "")
		embed = discord.Embed(title=c)
		await msg.channel.send(embed=embed)			
		return "EMBED"
	msg = await msg.channel.send(content)
	if random.random() > .99: await msg.author.send("the secret message dm euro for a doubley secret role, if you tell anyone how you got this the role will be taken away\nif you already have the role, you may choose to dm a screenshot of this message to someone, and they have the chance to get the role")	
	return msg

async def timers(msg, content, cmd="timers"):
	embed = discord.Embed(title="timers")
	for user, t in runningStopwatch.items():
		embed.add_field(name=user, value=round(time.time() - t, 2))
	await msg.channel.send(embed=embed)

async def levelMessage(msg, content, cmd="lvlmsg"):
	with open(levelingDataFilePath, "r+") as j:
		data = json.load(j)
		changeTo = content[len(cmd) + 2:].strip()
		userData = data[str(msg.author.id)]
		if testInContent(changeTo, "--see", "--get"):
			msg = await msg.channel.send(userData["message"])
		else:
			userData["message"] = changeTo
			clearFile(j)
			json.dump(data, j)
			msg = await msg.channel.send(f"changed to {changeTo}")
	return msg

async def cmdUsage(msg, content, cmd="commandusage"):
	if TICDelete(content): 
		await msg.delete()
		content = content.replace(DELETE, "")
	if testInContent(content, "--raw"):
		with open(commandusageFilePath, "rb") as j:
			return await msg.channel.send(file=discord.File(j, commandusageFilePath))
	with open(commandusageFilePath, "r") as j:
		data = json.load(j)
		if (split := splitContent(content, cmd, index=1).strip()):
			commandUse = data.get(split)
			if not commandUse:
				return await msg.channel.send("command not found")
			embed = discord.Embed(title=split)
			embed.add_field(name="times", value=commandUse)
			await msg.channel.send(embed=embed)
		else:
			embed = discord.Embed(title="TOP 10 USED COMMANDS")
			n = 1
			data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
			for k in data.keys():
				if n > 10: break
				embed.add_field(name=n, value=f'{k}: {data[k]}', inline=False)
				n += 1
			await msg.channel.send(embed=embed)

async def iq(msg, content, cmd="iq"):
	iq = random.randint(-3, 200)
	if TICDelete(content):
		await msg.delete()
		content = content.replace(DELETE, "")
	c = msg.author.mention if not splitContent(content, f'{cmd} ', index=1) else content[len(cmd) + 2:]
	await msg.channel.send(f'{c}\'s iq is *DRUMROLL*...')
	await asyncio.sleep(random.uniform(.7, 1.3))
	if msg.author.bot:
		msg = await msg.channel.send("i am computer i have [ERROR] iq")
	if iq == 200:
		msg = await msg.channel.send(f'you are the next einstein, you are smart enough to realize iq is dumb, so there is no need to say it')
	elif iq > 150:
		msg = await msg.channel.send(f"that's a pretty high iq: {iq}")
	elif iq > 50 and iq <= 150:
		msg = await msg.channel.send(iq)
	elif iq <= 50 and iq >= 0:
		msg = await msg.channel.send(f"you good there mate, your iq is {iq}")
	elif iq < 0:
		msg = await msg.channel.send(f"you literally don't have a brain you somehow have a negative iq idek\nIQ: {iq}")
	return msg

async def shrug(msg, content, cmd="shrug"):
	if TICDelete(content): await msg.delete()
	msg = await msg.channel.send(content=r"¯\_(ツ)_/¯")
	await asyncio.sleep(.3)
	await msg.edit(content=r"¯\\-(ツ)-/¯")
	await asyncio.sleep(.3)
	await msg.edit(content=r"¯\_(ツ)_/¯")

async def getUserData(user):
	with open(levelingDataFilePath, "r") as f:
		data = json.load(f)
		return data.get(str(user))

async def level(msg, content, cmd="level"):
	user = await getUserInContent(msg, content, cmd)
	if len(splitContent(content, " ")) > 1:
		user = discord.utils.get(msg.guild.members, id=user.id)
	userData = await getUserData(user.id)
	level = userData["level"]
	xp = userData["xp"]
	required = userData["required"]
	embed = discord.Embed(title=user.display_name, color=user.color)
	embed.add_field(name="level", value=level, inline=False)
	embed.add_field(name="xp", value=xp, inline=False)
	embed.add_field(name="required", value=required, inline=False)
	await msg.channel.send(embed=embed)

async def leaderboard(msg, content, cmd="top"):
	if testInContent(content, "--rawlevels"):
		with open(levelingDataFilePath, "rb") as f:
			await msg.channel.send(file=discord.File(f, levelingDataFilePath))
			return
	top = 10
	if TICDelete(content): 
		await msg.delete()
		content = content.replace(DELETE, "")
	if testInContent(content, " "):
		t = splitContent(content, " ", index=1)
		try: top = int(t)
		except: await msg.channel.send("NaN")
	with open(levelingDataFilePath, "r") as f:
		data = json.load(f)
		users = [(discord.utils.get(msg.guild.members, id=int(user)), int(data[user]["level"])) for user in data.keys()]
		users.sort(key=lambda x: x[1], reverse=True)
		embed = discord.Embed(title=f"Top {top}", color=users[0][0].color)
		firstPlaceRole = discord.utils.get(msg.guild.roles, name="first place (in crappy-off-brand leaderboards)")
		for n, user in enumerate(users):
			if firstPlaceRole in user[0].roles:
				await user[0].remove_roles(firstPlaceRole)
			if n > top - 1: break
			embed.add_field(name=str(n + 1) + " " + user[0].display_name, value=user[1], inline=False)

		await users[0][0].add_roles(firstPlaceRole)
		await msg.channel.send(embed=embed)


async def magicBall(msg, content, cmd="8ball"):
	if TICDelete(content): await msg.delete()
	with open(mballresponseFilePath, "r") as f:
		responses = f.read().split("\n")

	if testInContent(content, "--embed", "--e"):
		await msg.channel.send(embed=discord.Embed(title=random.choice(responses)))
	else: 
		return await msg.channel.send(f'Answer: {random.choice(responses)}')

async def spamCmd(msg, content, cmd="spam"):
	global Stop
	if Stop: Stop = False
	if isBot(msg, client): return ""

	c = content[len(cmd) + 2:]

	if TICDelete(c):
		await msg.delete()
		c = c.replace(DELETE, "")

	messages = c[:c.find(" ")]

	if not isInt(messages):
		return await msg.channel.send("not a valid number of messages")			

	if int(messages) > (lim := random.randint(40000, 110000)):
		return await msg.channel.send(f"pls consult a psychiatrist that's too many messages\nthe limit is: {lim}")		

	if int(messages) < 0: 
		return await msg.channel.send("ERROR: MESSAGE COUNT LESS THAN 0")

	if testInContent(c, "-random"):
		c = c.replace("-random", "")
		c = c[c.find(messages) + len(messages):]
		options = c.split(", ")
		return await spam(msg, int(messages), options)

	message = c[c.find(messages) + len(messages):]
	await spam(msg, int(messages), [message])

	if random.random() >= .99: await msg.channel.send("You found an easter egg hehe")
	else: await msg.channel.send(random.choice(["done", "Done"]))

async def randomFace(msg, content, cmd="randomface"):
	EYES = [":", ";"]
	MOUTHS = [")", "(", "{", "}", "[", "]", "p", "P", "d", "l", "C", "c"]
	return await oneLineCmd(msg, f'{random.choice(EYES)}{random.choice(MOUTHS)}' if random.random() >= .5 else f'{random.choice(MOUTHS)}{random.choice(EYES)}')

async def alphabet(msg, content, cmd="alphabet"):
	if testInContent(content, "--vowels"): send = "aeiou(y)"
	if testInContent(content, "--consonants"):
		send = "".join([x for x in string.ascii_lowercase if x not in "aeiou"])
	if random.random() > .98: send = "zyxwvutsrqponmlkjihgfedcba"
	msg = await oneLineCmd(msg, send)
	return msg

async def unicodeChar(msg, content, cmd="unicodechar"):
	amount = 1
	if TICDelete(content): 
		await msg.delete()
		content = content.replace(DELETE, "")

	if (split := splitContent(content, " ")):
		amount = split[1]
		if not isInt(amount):
			return await msg.channel.send("NaN")
		else: amount = int(amount)

	if "--value" in content:
		chars = [f"{chr('%s')} value: ({'%s'})" %random.randint(0, 185000) for _ in range(amount)]
	else: chars = [chr(random.randint(0, 185000)) for _ in range(amount)]
	
	return await msg.channel.send("\n".join(chars))

async def serverEmote(msg, content, cmd="serveremote"):
	amount = 1
	sep = "\n"
	if testInContent(content, "-sep"):
		sep = content.split("-sep ")[1]
	if isInt(splitContent(content.lower(), " ", index=1)): amount = int(splitContent(content.lower(), " ", index=1))
	sendE = [str(random.choice(client.emojis)) for _ in range(amount)]
	msg = await oneLineCmd(msg, sep.join(sendE))
	return msg

async def writeRoles(msg, content, cmd="doesnothing"):
	filename = splitContent(content.lower(), cmd, index=1)
	if TICDelete(filename):
		filename = filename.replace(DELETE, "")
		await msg.delete()

	with open(f".\\roles\\{filename}.txt", "w") as f:
		for x in client.get_all_members():
			try: f.write(f'\n{str(x.name)}\n')
			except: f.write(f"\n{x.id}\n")
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
				elif "Easter" in y.name:
					f.write("Easter")
				else:
					try: f.write(f'{y.name}\n')
					except: f.write("UNICODE\n")

	with open(f'.\\roles\\{filename}.txt', "rb") as f:
		await msg.channel.send(file=discord.File(f, f'{filename}.txt'))

async def spacer(msg, content, cmd="spacer"):
	await msg.delete()
	sep = " "
	c = splitContent(content.lower(), f'{cmd} ')[1]
	spaces = c[:c.find(" ")]
	c = c[c.find(" "):]
	if "-sep" in c:
		sep = splitContent(c, "-sep ", index=1)
		c = splitContent(c, " -sep", index=0)
	if not check_int(spaces):
		msg = await msg.channel.send(f"{spaces} is not a valid number of spaces")
		return msg
	add = sep * int(spaces)
	word = add.join(c)
	msg = await oneLineCmd(msg, word)
	return msg

async def upperLower(msg, content, cmd="upperlower"):
	mssg = content[len(cmd) + 2:]
	if not TICDelete(mssg): await msg.delete()
	else: mssg = mssg.replace(DELETE, "")

	newPhrase = []

	for val, letter in enumerate(mssg):
		if val > 0:
			if mssg[val - 1] != " " and newPhrase[val - 1].islower():
				letter = letter.upper()
			elif newPhrase[val - 2].islower() and mssg[val - 1] == " ":
				letter = letter.upper()
		newPhrase.append(letter)

	msg = await msg.channel.send("".join(newPhrase))
	return msg

async def startRPS(msg, content, cmd="rps"):
	opps = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
	setTo = {"r": "rock", "p": "paper", "scissors": "scissors"}
	t = 15
	if testInContent(content, "-time"):
		t = int(splitContent(content, "-time ", index=1).strip())
		if t >= 120:
			await msg.channel.send("sorry must be shorter than 2 minutes or 120 seconds")
			return 
	user1 = await client.fetch_user(msg.author.id)
	user2 = await client.fetch_user(splitContent(content, " ", index=1, func=lambda x: x[3:-1]))
	if user2 == client.user.id or user1 == client.user.id:
		await msg.channel.send(f"sorry {user1.mention} you have to face a real player")
	await user1.send(f"say your move here, you have {t} seconds (typos will mess up results)")
	await user2.send(f"say your move here, you have {t} seconds (typos will mess up results)")
	await asyncio.sleep(t)
	async for rep in user1.dm_channel.history(limit=1):
		resp1 = rep.content.lower()
		if resp1 == "--rand": resp1 = random.choice(list(opps.keys()))
	async for rep in user2.dm_channel.history(limit=1):
		resp2 = rep.content.lower()
		if resp2 == "--rand": resp2 = random.choice(list(opps.keys()))
	await msg.channel.send(f'{user1.mention} said {resp1}\n{user2.mention} said {resp2}')
	if resp1 == f"say your move here, you have {t} seconds (typos will mess up results)": 
		await msg.channel.send(f"{user1.name} didn't respond")
	if resp2 == f"say your move here, you have {t} seconds (typos will mess up results)":
		await msg.channel.send(f"{user2.name} didn't respond")

	if resp1 in setTo.keys(): resp1 = setTo[resp1]
	if resp2 in setTo.keys(): resp2 = setTo[resp2]

	if resp1 in opps.keys() and resp2 in opps.keys():
		if opps[resp2] == resp1:
			await msg.channel.send(f'{user2.mention} WINS')
		elif opps[resp1] == resp2:
			await msg.channel.send(f'{user1.mention} WINS')
		else: await msg.channel.send("ITS A DRAW")
	else: await msg.channel.send("either someone spelled something wrong, or someone isn't playing by the rules")

async def complexMessage(msg, content, cmd="complexmessage"):
	c = splitContent(content.lower(), cmd, index=1).split(", ")
	await msg.delete()
	try:
		send = c[0].strip().lower()
		filename = c[1]
		mssg = c[2]
	except: await msg.channel.send("make sure you give and seperate each paremeter with a ','")

	dm = True if send == "dm" else False
	send = False if send == "dm" else True

	if cmd == "message": filename = f'{filename}.txt'

	with open(f'.\\message\\{filename}', "w") as f:
		f.write(mssg)
	with open(f'.\\message\\{filename}', 'rb') as f:
		if send: await msg.channel.send(file=discord.File(f, filename))
		if dm:await msg.author.send(file=discord.File(f, filename))

async def sanity(msg, content, cmd="sanity"):
	c = content.split(cmd)[1]

	if TICDelete(c): 
		c = c.replace(f' {DELETE}', "")
		await msg.delete()

	if testInContent(c, "-r "):
		r = int(content.split("-r ")[1].split(" ")[0])
		c = c.split("-r ")[0]
	else: r = 3

	san = round(random.uniform(-1.5, 101), r)

	cases = {san > 100: f'{c} is so sane that they have become the universe itself',
				san >=49.5 and san <= 50.5: f'{c} is perfectly balanced between sane and insane',
				san < 0: f'how is {c} even alive'}
				
	if (case := cases.get(True)): msg = await msg.channel.send(case)
	else: msg = await msg.channel.send(f'{c} has {san}% sanity')
	return msg

async def coin(msg, content, cmd="coin"):
	if TICDelete(content): 
		await msg.delete()
		content = content.replace(DELETE, "")
	title = res = "heads" if random.random() >= .5 else "tails"
	if testInContent(content, "-bet"):
		bet = splitContent(content, "-bet")[1].strip()
		if bet == "t": bet = "tails"
		if bet == "h": bet = "heads"
		color, title = (0x00ff00, "YOU WIN") if res == bet else (0xff0000, "YOU LOSE")
	else:  color = 0xff00ff if res == "heads" else 0x0000ff
	
	embed = discord.Embed(title=title, color=color)
	await msg.channel.send(embed=embed)

async def roleInfo(msg, content, cmd="roleinfo"):
	if TICDelete(content):
		await msg.delete()
		content = content.replace(DELETE, "")
	rolename = splitContent(content, cmd + " ")[1]
	try:
		role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), msg.guild.roles)
		embed = discord.Embed(title=role.name, color=role.color)
		embed.add_field(name="Color", value=role.color)
		embed.add_field(name="Created at", value=await formatDateTime(role.created_at))
		await msg.channel.send(embed=embed)
	except AttributeError:
		await msg.channel.send("role not found")

async def roleCount(msg, content, cmd="rolecount"):
	c = str(content.split(cmd)[1].strip())
	Showroles = False
	if TICDelete(content):
		await msg.delete()
		c = c.replace(f' {DELETE}', "")
	if "--showroles" in c:
		Showroles = True
		c = c.replace(" --showroles", "") if c != "--showroles" else ""
	c = c[3:-1] if "<@!" in c else c
	if not c: c = str(msg.author.id)
	if (m := findMember(c, msg)):
		roles = [x.mention for x in m.roles]
		roleCount = len(roles) - 1
		if Showroles:
			embed = discord.Embed(title=f"{m.name}'s Roles")
			embed.add_field(name="Count", value=roleCount)
			embed.add_field(name="Roles", value="".join(roles))
			msg = await msg.channel.send(embed=embed)
		else: 
			msg = await msg.channel.send(roleCount)		
	else: msg = await msg.channel.send("User not found")
	return msg

async def rand(msg, content, cmd="rand"):
	if len(splitContent(content, cmd + " ")) > 1:
		c = content.split(" ")[1:]
		EVEN = "--even"
		ODD = "--odd"
		if TICDelete(" ".join(c)):
			await msg.delete()
			c.remove(DELETE)
		Even = True if testInContent(" ".join(c), EVEN) else False
		Odd = False if Even else True
		if Even: c.remove(EVEN)
		if Odd: c.remove(ODD)
		low = c[0].strip()
		high = c[1].strip()

		r = int(c[2].strip()) if len(c) == 3 else 15

		if not isInt(r):
			await msg.channel.send("you are not rounding to a whole number")				
			return ""

		if float(low) >= float(high):
			await msg.channel.send("Low must be lower than high")
			return ""

		if check_int(low) and check_int(high):
			while True:
				if Stop: await msg.channel.send(stop("stopped picking a number"))
				res = random.randint(int(low), int(high))
				if Even and res % 2 != 0: continue					
				if Odd and res % 2 == 0: continue
				else: break
		else:
			res = random.uniform(float(low), float(high))
			if r: res = round(res, r)
	else: res = random.randint(1, 10)
	msg = await msg.channel.send(res)
	return msg

async def compareRoles(msg, content, cmd="compareroles"):
	embed = discord.Embed(name="Role Comparison")
	c = content.split(testInContent(content, "comproles", "compareroles"), index=1).split(" ")
	user1 = str(c[1].strip()) 
	user2 = str(c[2].strip())
	if "<@!" in user1:
		user1 = str(user1)[3:-1]
	if "<@!" in user2:
		user2 = str(user2)[3:-1]
	u1name = findMember(user1, msg)
	u2name = findMember(user2, msg)
	if u1name and u2name:
		roles1 = {role.mention for role in u1name.roles}
		roles2 = {role.mention for role in u2name.roles}
		embed.add_field(name="both members", value="".join(roles1 & roles2))
		embed.add_field(name=u1name, value="".join(roles1 - roles2), inline=False)
		embed.add_field(name=u2name, value="".join(roles2 - roles1), inline=False)
		await msg.channel.send(embed=embed)
	else: await msg.channel.send("invalid name(s)")

async def family(msg, content, cmd="family"):
	with open("family.txt", "r") as f: await oneLineCmd(msg, f.read())

async def mballreply(msg, content, cmd="mballreply"):
	mssg = content.split(f'{cmd} ')[1]
	if userHasRole(msg, "mballresponseadder"):
		with open(mballresponseFilePath, "a") as f:
			f.write(mssg + "\n")
		msg = await msg.channel.send("message added")				
		return
	else: msg = await msg.channel.send("you don't have perms")
	return msg

async def mballDel(msg, content, cmd="8brdel"):
	reply = content.split(f"{cmd} ")[1]
	if userHasRole(msg, "mballresponseadder"):
		with open(mballresponseFilePath, "r+") as f:
			replies = f.read().split("\n")
			if reply in replies:
				replies.remove(reply)
				clearFile(f)
				f.write("\n".join(replies))
				await msg.channel.send(f'removed message: {reply}')
			else: await msg.channel.send("not a message")
	else: await msg.channel.send("you don't have perms")

async def count(msg, content, cmd="count"):
	await msg.delete()
	channel = discord.utils.get(msg.guild.channels, name="counting")
	highest = max([x.content.replace("*", "").replace("_", "").replace("`", "").strip(".") async for x in channel.history(limit=3)])
	highest = int(highest) + 1
	async for x in channel.history(limit=1):
		if isBot(x, client): return ""
	if (style := testInContent(content, "--i", "--b", "--ib", "--e", "--u", "--ui")):
		if style == "--i":
			await channel.send(f'*.{highest}.*')
		elif style == "--b":
			await channel.send(f'**.{highest}.**')
		elif style == "--ib":
			await channel.send(f'***.{highest}.***')
		elif style == "--u":
			await channel.send(f"__.{highest}.__")
		elif style == "--ui":
			await channel.send(f"___.{highest}.___")
		elif style == "--e":
			if testInContent(content, "-c"):
				color = splitContent(content, "-c ")[1]
				color = int(f'0x{color}', 16)
			else: color = 0x000000
			await channel.send(embed=discord.Embed(title=f'.{highest}.', color=discord.Color(color)))
	else: await channel.send(f'.{highest}.')

async def choose(msg, content, cmd="choose"):
	options = splitContent(content, f'{cmd} ')[1].split(", ")
	PICKS = "-picks "
	picks = 1
	for op in options:
		if PICKS in op.lower():
			picks = int(op.split(PICKS)[1])
			options[options.index(op)] = op.split(PICKS)[0]
			break
	choices = [random.choice(options) for _ in range(int(picks))]
	msg = await msg.channel.send("\n".join(choices))
	return msg

async def mball(msg, content, cmd="8ball"):
	if TICDelete(content): await msg.delete()
	with open(mballresponseFilePath, "rb") as f:
		await msg.channel.send(file=discord.File(f, "mballresponse.txt"))

async def pigLatin(msg, content, cmd="piglatin"):
	CASE = "--kc"
	content = content.replace(CASE, "") if testInContent(content, CASE) else content.lower()

	m = content.split(" ")[1:]

	if DELETE in m:
		await msg.delete()
		m.remove(DELETE)

	for n, word in enumerate(m):
		if word[0] in "aeiou": m[n] += "ay"
		else:
			moveToEnd = [None if letter in "aeiou" else letter for letter in word] 
			moveToEnd = moveToEnd[:moveToEnd.index(None)] #all the letters until the first vowel represented by None
			m[n] = f'{word[len(moveToEnd):]}{"".join(moveToEnd)}ay'
	msg = await msg.channel.send(" ".join(m))
	return msg

async def mostRoles(msg, content, cmd="mostroles"):
	global Stop
	if Stop: Stop = False
	c = content.split(cmd)[1]
	TOP = "-top "
	top = int(splitContent(content, TOP, index=1)) if TOP in c else 5
	if TICDelete(content): await msg.delete()

	memberRoles = {member.display_name.split("#")[0]: len(member.roles) - 1 for member in msg.guild.members}

	sortedKeys = sorted(memberRoles, key=memberRoles.get, reverse=True)
	top = [f'{r}, {memberRoles[r]}' for n, r in enumerate(sortedKeys) if n < top]
	msg = await msg.channel.send("\n".join(top))
	return msg

async def clear(msg, content, cmd="clear"):
	amnt = int(content[len(cmd) + 2:])
	perms = msg.author.guild_permissions.manage_messages
	if perms and msg.author.id != 579117856994623498:
		await msg.channel.purge(limit=amnt)
	else:
		await msg.channel.send(f"{msg.author.mention} you can't do that")
		for _ in range(random.randint(10, 15)):
			await msg.author.send("you cannot do that, don't do it again")

async def ridInvites(msg, content, cmd="clearinvites"):
	perms = msg.author.guild_permissions.create_instant_invite
	if perms:
		invites = await msg.guild.invites()
		for inv in invites:
			await inv.delete()
		return ""
	else: return await msg.channel.send("you don't have perms")

async def color(msg, content, cmd="color"):
	c = splitContent(content, f'{cmd}')[1].strip()
	if TICDelete(content):
		await msg.delete()
		c = c.replace(DELETE, "")
	if ", " in c:
		color = [int(x) for x in c.split(", ")]
		hexColor = [str(hex(x))[2:] for x in color]
		hexColor = list(map(lambda x: f'0{x}' if len(x) == 1 else x, hexColor))
		await msg.channel.send(embed=discord.Embed(title=f'#{"".join(hexColor)}', color=discord.Color.from_rgb(color[0], color[1], color[2])))			
		return ""
	if not c: c = str(msg.author.top_role)
	m = discord.utils.find(lambda r: r.name.lower() == c.lower(), msg.guild.roles)
	if m:
		embed = discord.Embed(title=str(m.color), color=m.color)
		await msg.channel.send(embed=embed)					
	else: await msg.channel.send("not a valid role")	

async def serverIcon(msg, content, cmd="servericon"):
	if TICDelete(content):	await msg.delete()
	embed = discord.Embed(title="Server icon", color=discord.Colour.from_rgb(180, 70, 180))
	embed.set_image(url=msg.guild.icon_url)
	await msg.channel.send(embed=embed)

async def channelInfo(msg, content, cmd="cc"):
	channel = msg.channel
	embed = discord.Embed(title=channel.name)
	if TICDelete(content):
		await msg.delete()
		content = content.repalce(DELETE, "")
	if splitContent(content, cmd)[1]:
		c = content.split(cmd)[1].strip()[2:-1]
		channel = discord.utils.get(msg.guild.channels, id=int(c))
	created = channel.created_at
	diff = datetime.datetime.now() - created
	pinCount = len(await channel.pins())
	if pinCount != 0: daysTillLastPin = (50-pinCount) / (pinCount / int(str(diff).split(" ")[0]))
	embed.add_field(name="Created at", value=await formatDateTime(created), inline=False)
	embed.add_field(name="Pins", value=pinCount, inline=False)
	if pinCount != 0: embed.add_field(name="days till last pin", value=str(daysTillLastPin), inline=False)
	embed.add_field(name="time since creation", value=diff)
	await msg.channel.send(embed=embed)

async def changes(msg, content, cmd="changes"):
	if TICDelete(content): await msg.delete()
	ver = splitContent(content, "-v ")[1].strip() if testInContent(content, "-v ") else None
	with open("CHANGELOG.txt", "r") as f:
		if not testInContent(content, "--nlatest") and not ver:
			c = f.read().split("\n")
			c = c[:c.index("====================================================================")]
		elif ver:
			c = f.read().split("\n")
			for lineN, line in enumerate(c):
				if ver == line.split(" ")[0]:
					c = c[lineN:c.index("====================================================================", lineN)]
					break
			else: return await msg.channel.send("did not find version")
		
		else: c = None

	with open("CHANGELOG.txt", "rb") as f:
		if testInContent(content, "--dms"): msg = await msg.author.send("\n".join(c)) if c else msg.author.send(file=discord.File(f, "changes.txt"))
		else: msg = await msg.channel.send("\n".join(c)) if c else await msg.channel.send(file=discord.File(f, "changes.txt"))
	return msg

async def commandCount(msg, content, cmd="commandcount"):
	with open("cmdslist.txt", "r") as f:
		cmds = len(f.read().split("\n")) - 2
	return await oneLineCmd(msg, cmds)

async def hexBinOct(msg, content, cmd="hex"):
	content = splitContent(content, cmd + " ")[1]
	num = list(map(lambda n: int(n), content.split(", "))) if ", " in content else [int(content)]
	repWith = {"hex": "0x", "bin": "0b", "oct": "0o"}[cmd]
	ans = list(map(lambda n: str(hex(n)).replace(repWith, ""), num))
	return await msg.channel.send(", ".join(ans))

async def response(msg, content, cmd="response", doFirst=False):
	global Stop
	if Stop: Stop = False
	if isBot(msg, client): return "is bot"
	limit = 1000
	mssg = content[len(cmd) + 2:].lower()
	if testInContent(mssg, "-lim"):
		limit = int(splitContent(mssg, "-lim ")[1].strip())
		if limit > 100000:
			return await msg.channel.send("you cannot go above 100k")
		mssg = splitContent(mssg, " -lim")[0]
	async with msg.channel.typing():
		hist = [m.content async for m in msg.channel.history(limit=limit)]
		responses = [hist[n - 1] for n, message in enumerate(hist) if message == mssg]
		if responses: msg = await msg.channel.send(f'{msg.author.mention} I HAVE FOUND A RESPONSE\n{random.choice(responses)}')
		else: msg = await msg.channel.send(f'did not find {mssg} in the past {limit} messages in this channel')
		return msg

async def timer(msg, content, cmd="stopwatch"):
	if TICDelete(content): await msg.delete()
	Running = runningStopwatch.get(msg.author.id)
	if not Running:
		runningStopwatch[msg.author.id] = time.time()
		await msg.channel.send(f'{msg.author.mention} stopawtch started')
	elif Running and testInContent(content, "--get"):
		await msg.channel.send(embed=discord.Embed(title=str(round(time.time() - Running, 2)) + " seconds"))
	elif Running:
		await msg.channel.send(embed=discord.Embed(title=str(round(time.time() - Running, 2)) + " seconds"))
		del runningStopwatch[msg.author.id]

async def emoteInfo(msg, content, cmd="emoteinfo"):
	emote = await msg.guild.fetch_emoji(int(content.split(":")[2][:-1]))
	embed = discord.Embed(title=emote.name)
	embed.add_field(name="Animated", value=emote.animated)
	embed.add_field(name="Added by", value=emote.user)
	embed.add_field(name="created at", value=await formatDateTime(emote.created_at))
	await msg.channel.send(embed=embed)

async def typeFor(msg, content, cmd="type"):
	timeToType = 5
	if (split := splitContent(content, " ")):
		timeToType = int(split[1])
	if timeToType > 420:
		return await msg.channel.send("sorry thats too long")
	async with msg.channel.typing():
		await asyncio.sleep(timeToType)
	return str(timeToType)

async def sendBlank(msg, content, cmd="sendblank"):
	amnt = 5
	if TICDelete(content):
		await msg.delete()
		content = content.replace(DELETE, "")
	if (split := splitContent(content, f"{cmd} ", index=1)):
		amnt = int(split)
	send = "_" + ("\n" * amnt) + "_"
	return await msg.channel.send(send)

async def hangman(msg, content, cmd="hangman"):
	user = (await getUserInContent(msg, content, cmd))
	if (split := splitContent(content, f'{cmd} ', index=1)): lives = int(split.strip())
	else: lives = 9
	await msg.author.send(f"you will have 15 seconds to send a word of your choice, and {user.name} will have to guess it in {msg.channel.name}")
	await asyncio.sleep(5)
	async for i in msg.author.dm_channel.history(limit=1):
		word = i.content
	disp = "".join(["-" if x not in [" ", "," "." "'" '"'] else x for x in word])
	playingHangman[user.id] = {"word": word, "lives": lives, "guessed": [], "disp": disp}
	return await msg.channel.send(disp)

async def runCommand(msg, content, cmd):
	DOFIRST = "-first "
	if DOFIRST in content:
		c = await runCommand(msg, content.split(DOFIRST)[1], splitContent(content, DOFIRST, index=1).split(" ")[0][1:])
		content = f'{content.split(f" {DOFIRST}")[0]} {c.content}'
		await c.delete()
	with open(commandusageFilePath, "r+") as j:
		data = json.load(j)
		try: data[cmd] += 1
		except: data[cmd] = 1
		clearFile(j)
		json.dump(data, j)
		
	if cmd == "timeit":
		start = time.time()
		await runCommand(msg, content.replace('[timeit ', ""), splitContent(content, "timeit ", index=1).split(" ")[0][1:])
		await msg.channel.send(time.time() - start)

	elif cmd == "ENDPLS":
		if msg.author.id == 334538784043696130:
			await msg.channel.send("Logging out")
			await client.logout()
		else: await msg.channel.send("smh you can't shut me down i have p o w e r over you")

	elif cmd == "secretcommand": await msg.channel.send("you have found a SECRET COMMAND do secretcommand + 10 for another command (10 doesn't equal 10 ;) )")
	elif cmd == "secretcommand2": await msg.channel.send("the final clue... save - e + 3")
	elif cmd == "sav3":
		await msg.channel.send("i have been lost for 15 years")
		await asyncio.sleep(1.2)
		await msg.channel.send("and now finally...")
		await asyncio.sleep(.6)
		await msg.channel.send("you have followed the secret clues and awoken me")
		await asyncio.sleep(1.5)
		await msg.channel.send("congratulations to anyone whitnessing this event, you earn a secret role a very epic secret role :) as my gift for saving me")
		await msg.channel.send("<!@334538784043696130> give them the role smh")

	elif cmd == "upupdowndownleftrightleftright":
		await msg.channel.send("what do you think this is some arcade machine with secret codes, lol")

	elif cmd == "timers": content = await timers(msg, content)
	elif cmd == "echo": content = await echo(msg, content)
	elif cmd == "ping": content = await ping(msg, content)
	elif cmd == "help": content = await hlp(msg, content)
	elif cmd in ["commandusage", "cmduse", "cmdusage", "commanduse"]: content = await cmdUsage(msg, content, cmd=cmd)
	elif cmd in ["findans", "equation", "result", "eval", "calc"]: content = await oneLineCmd(msg, eval(splitContent(content, cmd + " ", index=1)))
	elif cmd == "iq": content = await iq(msg, content)
	elif cmd == "shrug": content = await shrug(msg, content)
	elif cmd in ["level", "rank", "lvl"]: content = await level(msg, content, cmd=cmd)
	elif cmd == "top": content = await leaderboard(msg, content)
	elif cmd in ["magicball", "8ball", "7ball"]: content = await magicBall(msg, content, cmd=cmd)
	elif cmd == "spam": content = await spamCmd(msg, content)
	elif cmd in ["randomface","randface", "rface"]: content = await randomFace(msg, content, cmd=cmd)
	elif cmd in ["ttc", "thetroycommand"]: content = await oneLineCmd(msg, random.choice(["meow", "7", "**7**", "*7*", "mo"]))
	elif cmd in ["mmoney", "mymoney"]: content = await oneLineCmd(msg, f'{str(msg.author).split("#")[0]}, you have ${random.randint(0, 1000000)}')
	elif cmd in ["alphabet", "alpha"]: content = await alphabet(msg, content, cmd=cmd)
	elif cmd in ["ucodechar", "unicodechar"]: content = content = await unicodeChar(msg, content, cmd=cmd)
	elif cmd == "serveremote": content = await serverEmote(msg, content)
	elif cmd == "doesnothing": content = await writeRoles(msg, content)
	elif cmd == "spacer": content = await spacer(msg, content)
	elif cmd == "version": content = await oneLineCmd(msg, VERSION)
	elif cmd in ["upperlower", "ul"]: content = await upperLower(msg, content, cmd=cmd)
	elif cmd == "longmessage": content = await oneLineCmd(msg, "```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````hI```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
	elif cmd in ["rps", "rockpaperscissors"]: await startRPS(msg, content, cmd=cmd)
	elif cmd == "flush": content = await oneLineCmd(msg, f"{splitContent(content.lower(), f'{cmd} ')[1]} has been flushed down the toilet :toilet::toilet::toilet::toilet::toilet::toilet::toilet::toilet:")
	elif cmd in ["complexmessage", "message"]: content = await complexMessage(msg, content, cmd=cmd)
	elif cmd == "sanity": content = await sanity(msg, content)
	elif cmd == "coin": content = await coin(msg, content)
	elif cmd == "roleinfo": content = await roleInfo(msg, content)
	elif cmd == "rand": content = await rand(msg, content)
	elif cmd == "rolecount": content = await roleCount(msg, content)
	elif cmd in ["ship", "boat", "boip"]: content = await oneLineCmd(msg, "DISCLAIMER: I DO NOT SUPPORT SHIPPING PEOPLE IN ANY WAY, HOWEVER MY MASTER SEEMS TO HAVE OTHER PLANS" if random.random() >= .985 else f'{splitContent(content, ", ")[0].replace("[" + cmd + " ", "")[0:len(splitContent(content, ", ")[0].replace("[" + cmd + " ", "")) // 2]}{splitContent(content, ", ")[1][len(splitContent(content, ", ")[1]) // 2:]}')
	elif cmd in ["comproles", "compareroles"]: content = await compareRoles(msg, content, cmd=cmd)
	elif cmd == "family": content = await family(msg, content)
	elif cmd == "mballreply": content = await mballreply(msg, content)
	elif cmd == "8brdel": content = await mballDel(msg, content)			
	elif cmd == "count": content = await count(msg, content)
	elif cmd == "choose": content = await choose(msg, content)
	elif cmd in ["mballreplylist", "8ballreplylist", "8breplylist", "8brlist"]: content = await mball(msg, content, cmd=cmd)
	elif cmd == "reverse": content = await oneLineCmd(msg, splitContent(content, f'{cmd} ')[1][::-1])
	elif cmd in ["piglatin", "igpayatinlay"]: content = await pigLatin(msg, content, cmd=cmd)
	elif cmd == "mostroles": content = await mostRoles(msg, content)
	elif cmd == "imscared": content = await oneLineCmd(msg, random.choice(["don't be :smiling_imp:", "oh it's ok :)))))))))))))))))", "just don't pay attention of the sounds coming from your attic.....\nit's ok", "it's ok... he's comming :)"]))
	elif cmd == "clear": content = await clear(msg, content)
	elif cmd == "color": content = await color(msg, content)
	elif cmd == "servericon": content = await serverIcon(msg, content)
	elif cmd in ["cc", "channelcreated", "channelinfo", "ci"]: content = await channelInfo(msg, content, cmd=cmd)
	elif cmd == "changes": content = await changes(msg, content)					
	elif cmd in ["wiki", "wikipedia"]: content = await oneLineCmd(msg, f'https://en.wikipedia.org/wiki/Special:Search?search={content[len(cmd) + 2:].replace(" ", "_")}')
	elif cmd == "commandcount": content = await commandCount(msg, content)
	elif cmd in ["hex", "bin", "oct"]: content = await hexBinOct(msg, content, cmd=cmd)
	elif cmd == "tof": content = await oneLineCmd(msg, 9 / 5 * float(splitContent(content, cmd + " ", index=1)) + 32)
	elif cmd == "toc": content = await oneLineCmd(msg, 5 / 9 * (float(splitContent(content, cmd + " ", index=1)) - 32))
	elif cmd == "response": content = await response(msg, content)
	elif cmd in ["stopwatch", "timer"]: content = await timer(msg, content, cmd=cmd)
	elif cmd == "lvlmsg": content = await levelMessage(msg, content)
	elif cmd == "emoteinfo": content = await emoteInfo(msg, content)
	elif cmd == "avatar": content = await msg.channel.send(getUserInContent(msg, content, cmd).avatar_url)
	elif cmd == "slowdown": content = await echo(msg, cmd + " **Slow Down** 🐌", cmd="slowdown")
	elif cmd == "fetchuser": content = await msg.channel.send((await client.fetch_user(int(splitContent(content, f'{cmd} ', index=1)))).name)
	elif cmd == "clearinvites": content = await ridInvites(msg, content)
	elif cmd == "typefor": content = await typeFor(msg, content)
	elif cmd == "hangman": content = await hangman(msg, content)
	elif cmd == "sendblank": content = await sendBlank(msg, content)
	elif cmd == "daily": content = await oneLineCmd(msg, f"you earned ${random.randint(0, 1000000)} you can use this command once a day!")
	else: 
		with open(commandusageFilePath, "r+") as j:
			data = json.load(j)
			del data[cmd]
			clearFile(j)
			json.dump(data, j)
		content = await msg.channel.send(f'{cmd} {random.choice(["is not a thing", "does not exist"])}')
	return content

@client.event
async def on_ready():
	global blueCheck, neutral
	await client.change_presence(activity=discord.Game(f'version: {VERSION}'))
	blueCheck = discord.utils.get(client.emojis, name="Blue_check")
	neutral = discord.utils.get(client.emojis, name="neutral")

	print(f"ONLINE\nversion: {VERSION}")

@client.event
async def on_message(msg):
	global Stop, playingGuessingGame
	global blueCheck, neutral

	if msg.author.bot and Stop:
		Stop = False
		return

	if msg.author.id == 311621977339068418 and msg.channel.id not in (715043261110288415, 658815060646297659):
		await msg.delete()
		print("message deleted")

	content = msg.content
	if not content: return

	if testInContent(content, "---delete", "—-delete"): await msg.delete()
	if testInContent(content, "---delin "):
		t = splitContent(content, "---delin ", index=1).strip()
		try: await asyncio.sleep(int(t))
		except: 
			await msg.channel.send("NaN")
			return 
		await msg.delete()

	if msg.channel.id == 427973752647712768 or testInContent(content, "---chkx", "---reactchkx"):
		await msg.add_reaction(blueCheck)
		await msg.add_reaction(neutral)
		await msg.add_reaction("❌")

	if random.random() >= .9994: 
		if isBot(msg, client): return
		await msg.channel.send(random.choice(["mhm", "interesting", "fascinating", "very cool"]))
		
	if content == f'is <@!{client.user.id}> a bot' or content == f'are you a bot <@!{client.user.id}>':
		await msg.channel.send(f"no {discord.utils.get(client.emojis, name='Watching1')}")
		return

	if f"<@!{client.user.id}>" in content:
		await msg.channel.send(random.choice([discord.utils.find(lambda e: e.name.lower() == "watching1", client.emojis), discord.utils.find(lambda e: e.name.lower() == "pinged", client.emojis)]))
		
	await giveXP(msg)
	await reduceXP(msg)

	if content[0] in PREFIX:

		cmd = getCmd(content)

		#ongoing events			
		if cmd == "guessinggame":
			c = splitContent(content, cmd)[1]
			low, high, lives = 1, 100, 5
			if len(c) > 0:
				c = c.split(" ")
				c.pop(0)
				low = int(c[0])
				high = int(c[1])
				if len(c) >= 3: lives = int(c[2])
			ans = random.randint(low, high)
			await msg.channel.send("guess")
			playingGuessingGame[msg.author.id] = {"ans": ans, "lives": lives}
			return ""

		elif cmd == "reactiontime":
			await msg.channel.send("i will say GO and you have to send something as fast as possible (probably prepare the message before hand)")
			reacting[msg.author.id] = 0
			await asyncio.sleep(random.uniform(1.5, 6))
			reacting[msg.author.id] = time.time()
			await msg.channel.send("GO")
			return
		elif cmd == "stop":
			if TICDelete(content): await msg.message.delete()
			Stop = True
		else: await runCommand(msg, content, cmd)

	if reacting.get(msg.author.id):
		await msg.channel.send(f'{msg.author.mention} your reaction time is {time.time() - reacting[msg.author.id] - client.latency} seconds')
		del reacting[msg.author.id]

	if playingGuessingGame.get(msg.author.id):
		c = msg.content
		ans = playingGuessingGame[msg.author.id]["ans"]
		lives = playingGuessingGame[msg.author.id]["lives"]
		if c in ["stop", "giveup", "cancel"]:
			await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(100, 0, 0)))
			del playingGuessingGame[msg.author.id]
		elif isInt(c):
			lives -= 1
			if lives <= 0:
				if int(content) == ans:
					await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} ITS A DRAW', color=discord.Color.from_rgb(155, 155, 155)))
				else: await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(255, 0, 0)))
				del playingGuessingGame[msg.author.id]
			elif int(content) == ans:
				await msg.channel.send(embed=discord.Embed(title=f"{msg.author.display_name} YOU WIN\nWITH {lives} LIVES LEFT", color=discord.Color.from_rgb(0, 255, 0)))
				del playingGuessingGame[msg.author.id]
				return ""
			await msg.channel.send("too high" if int(c) > ans else "too low")
		else: await msg.channel.send("NaN")
		playingGuessingGame[msg.author.id]["lives"] = lives
		await msg.channel.send(f"guess\nyou have {lives} lives left")

	if playingHangman.get(msg.author.id):
		tempWord = playingHangman[msg.author.id]["word"]
		tempLives = playingHangman[msg.author.id]["lives"]
		tempDisp = playingHangman[msg.author.id]["disp"]
		if content in tempWord:
			foo = [x for x in tempDisp]
			for n, w in enumerate(tempWord):
				if content == w:
					foo[n] = w
			tempDisp = "".join(foo)
		else:
			tempLives -= 1
		if tempLives <= 0 and tempDisp == tempWord:
			await msg.channel.send(f"ITS A DRAW\nThe word was {tempWord}\n{msg.author} ran out of lives but guessed the word")
			del playingHangman[msg.author.id]
		elif tempLives <= 0:
			await msg.channel.send(f'YOU LOSE\nThe word was {tempWord}')
			del playingHangman[msg.author.id]
		elif tempDisp == tempWord:
			await msg.channel.send(f'YOU WIN\nYou won with {tempLives} left!')
			del playingHangman[msg.author.id]
		else: await msg.channel.send(f'Guesses left: {tempLives}\nKnown word: {tempDisp}')
		playingHangman[msg.author.id] = {"word": tempWord, "lives": tempLives, "disp": tempDisp}

@client.event
async def on_voice_state_update(member, before, after):
	if not before.channel and after.channel:
		role = discord.utils.get(member.guild.roles, name="vc")
		await member.add_roles(role)
	elif before.channel and not after.channel:
		role = discord.utils.get(member.guild.roles, name="vc")
		await member.remove_roles(role)
	
client.run(token)