import discord
from discord.ext import commands
import time, datetime
import random
import string
import pyautogui
import wikipedia
import asyncio
import json

#TODO: convert every command into a funcion, and try to make it so that if you do [spam [piglatin hi it would do the piglatin first then spam the result of piglatin
#^ maybe eventually

DELETE = "--delete"
VERSION = "2.6.1.1"
Stop = False

playingGuessingGame = {}
runningTimer = {}
reacting = {}

PREFIX = "["

token = "NjQxNzk1NjU2Mzc3MTcyMDAw.XcNk8g.HEvnaXjuXFQhN1iilaaffbiPcoo"

client = commands.Bot(command_prefix=PREFIX)

BASICINFO = {"level": 1, "xp": 0, "required": 100, "lastTalked": 0}

equation = "level * 1000"

def isBot(msg, client):
	if msg.author == client.user: return True
	if msg.author.bot: return True
	return False

async def giveXP(msg):
	if isBot(msg, client): return
	with open("levelingData.json", "r+") as f:
		data = json.load(f)
		if data.get(str(msg.author.id)):
			userInfo = data[str(msg.author.id)]
			lastTalked = int(userInfo["lastTalked"])
			if time.time() - lastTalked >= 60:
				level = userInfo["level"]
				xp = userInfo["xp"]
				xp += random.randint(15, 100)
				lastTalked = time.time()
				required = userInfo["required"]
				if xp >= required:
					level += 1
					xp //= 2
					await msg.channel.send(f'{msg.author.mention} you have leveled up to level {level}, very cool')
				required = eval(equation)
				userInfo = {"level": level, "xp": xp, "required": required, "lastTalked": lastTalked}
			data[str(msg.author.id)] = userInfo
		else:
			data[str(msg.author.id)] = BASICINFO
			data[str(msg.author.id)]["lastTalked"] = time.time()
		clearFile(f)
		json.dump(data, f)

async def reduceXP(msg):
	if isBot(msg, client): return
	with open("levelingData.json", "r+") as f:
		data = json.load(f)
		for user in data.keys():
			if time.time() - data[user]["lastTalked"] >= 43200:
				if data[user]["xp"] > 0:
					data[user]["xp"] -= random.randint(0, 1)
				if data[user]["xp"] <= (data[user]["level"] * 1000) // 2 and data[user]["level"] > 0:
					data[user]["level"] -= 1
					data[user]["xp"] = (data[user]["level"] * 1000) // 2 + 1500
		clearFile(f)
		json.dump(data, f)

def testInContent(content, *testfor):
	for x in testfor:
		if x.lower() in content.lower():
			return x
	return ""
	
def TICDelete(content):
	return testInContent(content, DELETE)

def getCmd(content):
	return content.split(" ")[0][1:]				

def splitContent(content, *split, index=None):
	for x in split:
		if x in content:
			if index:
				return content.split(x)[index]
			return content.split(x)
	return ""

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def stop(*args, **kwargs):
	global Stop
	Stop = False
	if args: return random.choice(args)

def userHasRole(msg, *role):
	if discord.utils.find(lambda r: role in r, msg.author.roles):
		return True
	return False

def isInt(testee):
	try:
		int(testee)
		return True
	except:	return False

def findMember(c, msg):
	return discord.utils.find(lambda m: str(m.id) == c or str(m.display_name.split("#")[0].lower()) == c.lower(), msg.guild.members)

def clearFile(file):
	file.seek(0)
	file.truncate()

async def spam(msg, messages, message, BlockStop=False):
	global Stop
	for _ in range(int(messages)):
		if Stop and not BlockStop:
			await msg.channel.send(stop("stopped spam", "Stopped spam"))
			return ""
		await msg.channel.send(random.choice(message))
		await asyncio.sleep(random.uniform(.6, 1.3))

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(f'version: {VERSION}'))
	print(f"ONLINE\nversion: {VERSION}")

@client.event
async def on_message(msg):
	global Stop, playingGuessingGame

	content = msg.content

	if msg.author.id == 469703194751008768 and content in ["people know me as weird gif girl", "im known as weird gif girl", "ppl call me weird gif girl", "ppl know me as weird gif girl"]:
		msg.channel.send("nice to meet you ghostly")

	if msg.author.id == 311621977339068418 and msg.channel.id not in (658815060646297659, 476977066839900165):
		await msg.delete()
		print("message deleted")

	if not content: return

	if random.random() >= .998: 
		if isBot(msg, client): return
		await msg.channel.send(random.choice(["mhm", "interesting", "fascinating", "very cool"]))
		
	if content == f'is <@!{client.user.id}> a bot' or content == f'are you a bot <@!{client.user.id}>':
		await msg.channel.send("no <:Watching1:697677860336304178>")
	if f"<@!{client.user.id}>" in content:
		await msg.channel.send(random.choice([discord.utils.find(lambda e: e.name.lower() == "watching1", client.emojis), discord.utils.find(lambda e: e.name.lower() == "pinged", client.emojis)]))

	await giveXP(msg)
	await reduceXP(msg)

	if content[0] in PREFIX:

		cmd = getCmd(content)

		with open("commandusage.json", "r+") as j:
			data = json.load(j)
			try: data[cmd] += 1
			except: data[cmd] = 1
			clearFile(j)
			json.dump(data, j)

		if cmd == "ENDPLS":
			if msg.author.id == 334538784043696130:
				await msg.channel.send("Logging out")
				await client.logout()
			else: await msg.channel.send("smh you can't shut me down i have p o w e r over you")

		elif cmd == "secretcommand":
			await msg.channel.send("you have found a SECRET COMMAND do secretcommand + 10 for another command (10 doesn't equal 10 ;) )")

		elif cmd == "secretcommand2":
			await msg.channel.send("the final clue... save - e + 3")
		
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

		elif cmd == "rawlevels":
			with open("levelingData.json", "rb") as f:
				await msg.channel.send(file=discord.File(f, "levelingData.json"))

		elif cmd == "timers":
			embed = discord.Embed(title="timers")
			for user, t in runningTimer.items():
				embed.add_field(name=user, value=round(time.time() - t, 2))
			await msg.channel.send(embed=embed)

		elif cmd in ["commandusage", "cmduse", "cmdusage", "commanduse"]:
			if TICDelete(content): 
				await msg.delete()
				content = content.replace(DELETE, "")
			split = splitContent(content, cmd)[1].strip()
			with open("commandusage.json", "r") as j:
				data = json.load(j)
				if split:
					commandUse = data.get(split)
					if not commandUse:
						await msg.channel.send("command not found")
						return
					embed = discord.Embed(title=split)
					embed.add_field(name="times", value=commandUse)
					await msg.channel.send(embed=embed)
					return
				else:
					embed = discord.Embed(title="TOP 10 USED COMMANDS")
					n = 1
					data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
					for k in data.keys():
						if n > 10: break
						embed.add_field(name=n, value=f'{k}: {data[k]}', inline=False)
						n += 1
					await msg.channel.send(embed=embed)

		elif cmd == "end": await msg.channel.send("end")

		elif cmd == "help":
			categories = ["HELP", "FUN", "GAMES", "RANDOM", "MATHY", "INFO", "MISC", "INTERESTING", ""]
			print(splitContent(content, cmd + " ", index=1).upper())
			if splitContent(content, cmd + " ", index=1).upper() in categories:
				with open("cmdslist.txt", "r") as f:
					embed = discord.Embed(title="Help", color=discord.Color(0x00ffe2))
					cat = splitContent(content, cmd + " ")
					read = f.read().split("\n")
					val = {}
					if not cat:
						for n, line in enumerate(read):
							if line.isupper():
								val[line] = []
								cat = line
								continue
							val[cat].append(line)
						for k in val.keys():
							embed.add_field(name=k, value="\n".join(val[k]), inline=False)
					else:
						cat = cat[1].upper().strip()
						LN = 1000
						for n, line in enumerate(read):
							if line.isupper() and line == cat:
								val[cat] = []
								LN = n
							if line.isupper() and n > LN:
								print(val)
								embed.add_field(name=cat, value="\n".join(val[cat]))
								break
							if val and LN != n:
								val[cat].append(line)
					await msg.channel.send(embed=embed)

			elif len(splitContent(content, " ")) > 1 and "--all" not in content:
				command = splitContent(content, " ")[1]
				with open("helpMsg.txt") as f:
					c = f.read().split("\n")
					startLN = 0
					endLN = 0
					for n, line in enumerate(c):
						if startLN and line == "":
							endLN = n
							break
						if command == line.split(" ")[0]: startLN = n
					else:
						await msg.channel.send("command not found")
						return ""
					text = ""
					for n, lineText in enumerate(c):
						if n + 1 >= startLN and n + 1 <= endLN:
							text += f'{lineText}\n'
						if n+1 >= endLN: break
					await msg.channel.send(embed=discord.Embed(title=text, color=discord.Colour(0x00ffe2)))
					return ""

			elif testInContent(content, "--all"):
				with open("helpMsg.txt", "rb") as f:
					await msg.channel.send(file=discord.File(f, "helpMsg.txt"))

		elif cmd in ["findans", "equation", "result", "eval"]:
			eq = splitContent(content, cmd + " ")[1]
			await msg.channel.send(eval(eq))

		elif cmd == "shrug":
			if TICDelete(content): await msg.delete()
			msg = await msg.channel.send(content=r"¯\_(ツ)_/¯")
			await asyncio.sleep(.3)
			await msg.edit(content=r"¯\\-(ツ)-/¯")
			await asyncio.sleep(.3)
			await msg.edit(content=r"¯\_(ツ)_/¯")

		elif cmd in ["level", "rank"]:
			c = str(content.split(cmd)[1].strip())
			c = c[3:-1] if "<@!" in c else c
			if not c: c = str(msg.author.id)
			user = findMember(c, msg)
			user = msg.author if not user else user
			if len(splitContent(content, " ")) > 1:
				user = discord.utils.get(msg.guild.members, id=user.id)
			with open("levelingData.json", "r") as f:
				data = json.load(f)
				userData = data[str(user.id)]
				level = userData["level"]
				xp = userData["xp"]
				required = userData["required"]
				users = [(discord.utils.get(msg.guild.members, id=int(user)).display_name, int(data[user]["level"])) for user in data.keys()]
				users.sort(key=lambda x: x[1], reverse=True)
				pos = users.index((user.display_name, level))
				embed = discord.Embed(title=user.display_name, color=user.color)
				embed.add_field(name="level", value=level, inline=False)
				embed.add_field(name="xp", value=xp, inline=False)
				embed.add_field(name="required", value=required, inline=False)
				embed.add_field(name="position", value=pos + 1, inline=False)
				await msg.channel.send(embed=embed)

		elif cmd == "top":
			with open("levelingData.json", "r") as f:
				data = json.load(f)
				users = [(discord.utils.get(msg.guild.members, id=int(user)), int(data[user]["level"])) for user in data.keys()]
				users.sort(key=lambda x: x[1], reverse=True)
				if data[str(users[0][0].id)]["level"] == data[str(users[1][0].id)]["level"]:
					if data[str(users[0][0].id)]["xp"] <= data[str(users[1][0].id)]["xp"]:
						first = users.pop(1)
						users.insert(0, first)
				embed = discord.Embed(title="Top 10", color=users[0][0].color)
				firstPlaceRole = discord.utils.get(msg.guild.roles, name="first place (in crappy-off-brand leaderboards)")
				for n, user in enumerate(users):
					if firstPlaceRole in user[0].roles:
						await user[0].remove_roles(firstPlaceRole)
					if n > 9: break
					embed.add_field(name=str(n + 1) + " " + user[0].display_name, value=user[1], inline=False)

				await users[0][0].add_roles(firstPlaceRole)
				await msg.channel.send(embed=embed)

		elif cmd == "ping":
			if "<@" in content:
				await msg.channel.send("are you trying to ping someone..... don't do that. :/")
				return ""
			if TICDelete(content): await msg.delete()

			if random.random() >= .95:
				await msg.author.send("upupdowndownleftrightleftright")
				await asyncio.sleep(5)
				await msg.author.send("OH SHOOT I WASNT SUPPOSED TO SAY TH-")
				await asyncio.sleep(1)
				await msg.author.send("goodbye")

			if random.random() >= .99:
				await msg.channel.send("uh yeah tbh i don't really know what this does, like i have an idea but like idk")
			elif random.random() >= .97:
				await msg.channel.send("LOL GET PRANKD THIS DOES NOTHING ROFL XD XD XD XD XD")
			else: await msg.channel.send(f':ping_pong: {round(client.latency * 1000)}ms')	

		elif cmd == "echo":
			if not TICDelete(content): 
				await msg.delete()
				content = content.replace(DELETE, "")
			if testInContent(content, "--embed"):
				c = content.replace(" --embed", "")
				embed = discord.Embed(title=splitContent(c, cmd)[1])
				await msg.channel.send(embed=embed)			
				return ""
			if random.random() > .99: await msg.author.send("the secret message dm euro for a doubley secret role, if you tell anyone how you got this the role will be taken away\nif you already have the role, you may choose to dm a screenshot of this message to someone, and they have the chance to get the role")
			await msg.channel.send(splitContent(content, cmd)[1])

		elif cmd in ["magicball", "8ball", "7ball"]:
			if TICDelete(content): await msg.delete()
			with open("mballresponse.txt", "r") as f:
				responses = f.read().split("\n")

			if testInContent(content, "--embed", "--e"):
				await msg.channel.send(embed=discord.Embed(title=random.choice(responses)))
			else: await msg.channel.send(f'Answer: {random.choice(responses)}')

		elif cmd == "spam":
			if Stop: Stop = False
			if isBot(msg, client): return ""

			c = splitContent(content, f"{cmd} ")[1]

			if TICDelete(c):
				await msg.delete()
				c = c.replace(DELETE, "")

			lim = random.randint(40000, 110000)
			messages = c[:c.find(" ")]

			if not isInt(messages):
				await msg.channel.send("not a valid number of messages")			
				return ""
			if int(messages) > lim:
				await msg.channel.send(f"pls consult a psychiatrist that's too many messages\nthe limit is: {lim}")		
				return ""

			message = c[c.find(messages) + len(messages):]

			if testInContent(c, "-random"):
				c = c.replace("-random", "")
				c = c[c.find(messages) + len(messages):]
				options = c.split(", ")
				await spam(msg, int(messages), options)
				await msg.channel.send(random.choice(["done", "Done"]))
				return ""

			if message.lower() == "done":
				await msg.channel.send(random.choice(["HAHA NICE TRY FOOLING EVERYONE WITH THE DONE", "nope can't say that", "you cannot say 'done'"]))				
				return ""

			await spam(msg, int(messages), [message])

			if random.random() >= .99:
				await msg.channel.send("You found an easter egg hehe")
			else:
				await msg.channel.send(random.choice(["done", "Done"]))

		elif cmd in ["randomface","randface", "rface"]:
			if TICDelete(content): await msg.delete()
			EYES = [":", ";"]
			MOUTHS = [")", "(", "{", "}", "[", "]", "p", "P", "d", "l"]
			send = f'{random.choice(EYES)}{random.choice(MOUTHS)}' if random.random() >= .5 else f'{random.choice(MOUTHS)}{random.choice(EYES)}'
			await msg.channel.send(send)

		elif cmd in ["ttc", "thetroycommand"]:
			if TICDelete(content): await msg.delete()
			await msg.channel.send(random.choice(["meow", "7", "**7**", "*7*", "mo"]))

		elif cmd in ["mmoney", "mymoney"]:
			if TICDelete(content): await msg.delete()
			await msg.channel.send(f'{str(msg.author).split("#")[0]}, you have ${random.randint(0, 1000000)}')

		elif cmd in ["alphabet", "alpha"]:
			if TICDelete(content): await msg.delete()
			if random.random() > .98: await msg.channel.send("zyxwvutsrqponmlkjihgfedcba")
			else: await msg.channel.send("abcdefghijklmnopqrstuvwxyz")

		elif cmd in ["ucodechar", "unicodechar"]:
			amount = 1
			if TICDelete(content): 
				await msg.delete()
				content = content.replace(DELETE, "")
			if testInContent(content, " "):
				amount = splitContent(content, " ")[1]
				if not isInt(amount):
					await msg.channel.send("NaN")
					return
				else: amount = int(amount)
				
			if "--value" in content:
				chars = [f"{chr('%s')} value: ({'%s'})" %random.randint(0, 185000) for _ in range(amount)]
			else: chars = [chr(random.randint(0, 185000)) for _ in range(amount)]
			
			await msg.channel.send("\n".join(chars))
	
		elif cmd == "serveremote":
			try: amount = int(content.lower().split(" ")[1])
			except: amount = 1
			if TICDelete(content): await msg.delete()
			sendE = [random.choice(client.emojis).mention for _ in range(amount)]
			await msg.channel.send("\n".join(sendE))

		elif cmd == "doesnothing":
			filename = splitContent(content.lower(), cmd)[1]
			if TICDelete(filename):
				filename = filename.replace(DELETE, "")
				await msg.delete()

			with open(f".\\roles\\{filename}.txt", "w") as f:
				for x in client.get_all_members():
					try: f.write(f'{str(x.name)}\n')
					except: f.write("UNWRITEABLE")
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

		elif cmd == "spacer":
			sep = " "
			c = splitContent(content.lower(), f'{cmd} ')[1]
			spaces = c[:c.find(" ")]
			c = c[c.find(" "):]
			if "-sep" in c:
				sep = splitContent(c, "-sep ")[1]
				c = splitContent(c, " -sep")[0]
			if not isInt(spaces):
				await msg.channel.send(f"{spaces} is not a valid number of spaces")
				return
			await msg.delete()
			spaces = int(spaces)
			add = sep * spaces
			word = add.join(c)
			await msg.channel.send(word)

		elif cmd == "version":
			if TICDelete(content): await msg.delete()
			await msg.channel.send(VERSION)

		elif cmd in ["upperlower", "ul"]:
			mssg = " ".join(content.lower().split(PREFIX + f"{cmd} ")[1::])
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

			await msg.channel.send("".join(newPhrase))

		elif cmd == "longmessage":
			if TICDelete(content): await msg.delete()
			await msg.channel.send("```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````hI```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")

		elif cmd in ["rps", "rockpaperscissors"]:
			opps = {"rock": "scissors", "paper": "rock", "scissors": "paper", "r": "scissors", "p": "rock", "s": "paper"}

			t = 15
			if testInContent(content, "-time"):
				t = int(splitContent(content, "-time ")[1].strip())
				if t >= 120:
					await msg.channel.send("sorry must be shorter than 2 minutes or 120 seconds")
					return 
			user1 = await client.fetch_user(msg.author.id)
			user2 = await client.fetch_user(splitContent(content, " ")[1][3:-1])
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
			if resp1 == f"say your move here, you have {t} seconds (typos will mess up results)": 
				await msg.channel.send(f"{user1.name} didn't respond")
			if resp2 == f"say your move here, you have {t} seconds (typos will mess up results)":
				await msg.channel.send(f"{user2.name} didn't respond")
			await msg.channel.send(f'{user1.mention} said {resp1}\n{user2.mention} said {resp2}')

			if resp1 in opps.keys() and resp2 in opps.keys():
				if resp1 == resp2:
					await msg.channel.send("ITS A DRAW")
				elif opps[resp1] == resp2:
					await msg.channel.send(f'{user1.mention} WINS')
				else:
					await msg.channel.send(f'{user2.mention} WINS')
			else:
				await msg.channel.send("either someone spelled something wrong, or someone isn't playing by the rules")

		elif cmd == "flush":
			flushee = splitContent(content.lower(), f'{cmd} ')[1]
			if TICDelete(flushee): 
				flushee = flushee.replace(DELETE, "")
				await msg.delete()
			await msg.channel.send(flushee + " has been flushed down the toilet :toilet::toilet::toilet::toilet::toilet::toilet::toilet::toilet:")

		elif cmd == "stop":
			if TICDelete(content): await msg.message.delete()
			Stop = True

		elif cmd == "complexmessage":
			c = content.lower().split(cmd)[1].split(", ")
			await msg.delete()
			try:
				send = c[0].strip().lower()
				filename = c[1]
				mssg = c[2]
			except: await msg.channel.send("make sure you give and seperate each paremeter with a ','")

			if send == "dm":
				dm = True
				send = False
			else:
				send = True
				dm = False
				
			with open(f'.\\message\\{filename}', "w") as f:
				f.write(mssg)
			if send:
				with open(f'.\\message\\{filename}', 'rb') as f:
					await msg.channel.send(file=discord.File(f, filename))
			if dm:
				with open(f'.\\message\\{filename}', 'rb') as f:
					await msg.author.send(file=discord.File(f, filename))

		elif cmd == "message":
			c = content.lower().split(cmd)[1].split(", ")
			try:
				send = c[0].strip().lower()
				filename = c[1]
				mssg = c[2]
			except: await msg.channel.send("make sure you give and seperate each paremeter with a ','")

			if send == "dm":
				dm = True
				send = False
			else:
				send = True
				dm = False

			await msg.delete()

			with open(f'.\\message\\{filename}.txt', "w") as f:
				f.write(mssg)
			if send:
				with open(f'.\\message\\{filename}.txt', 'rb') as f:
					await msg.channel.send(file=discord.File(f, f'{filename}.txt'))
			if dm:
				with open(f'.\\message\\{filename}.txt', 'rb') as f:
					await msg.author.send(file=discord.File(f, f'{filename}.txt'))

		elif cmd == "sanity":
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
					 
			for case in cases.keys():
				if case:
					await msg.channel.send(cases[case])
					break
			else: await msg.channel.send(f'{c} has {san}% sanity')

		elif cmd == "coin":
			if TICDelete(content): 
				await msg.delete()
				content = content.replace(DELETE, "")
			title = res = "heads" if random.random() >= .5 else "tails"
			if testInContent(content, "-bet"):
				bet = splitContent(content, "-bet")[1].strip()
				if bet == "t": bet = "tails"
				if bet == "h": bet = "heads"
				if res == bet:
					color = 0x00ff00
					title = "YOU WIN"
				else:
					title = "YOU LOSE"
					color = 0xff0000
			else: 
				color = 0xff00ff if res == "heads" else 0x0000ff
			
			embed = discord.Embed(title=title, color=color)
			await msg.channel.send(embed=embed)

		elif cmd == "roleinfo":
			if TICDelete(content):
				await msg.delete()
				content = content.replace(DELETE, "")
			rolename = splitContent(content, cmd + " ")[1]
			try:
				role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), msg.guild.roles)
				embed = discord.Embed(title=role.name, color=role.color)
				embed.add_field(name="Color", value=role.color)
				embed.add_field(name="Created at", value=role.created_at)
				await msg.channel.send(embed=embed)
			except AttributeError:
				await msg.channel.send("role not found")

		elif cmd == "rand":
			if Stop: Stop = False
			if len(splitContent(content, cmd + " ")) > 1:
				c = content.split(" ")[1:]
				EVEN = "--even"
				ODD = "--odd"
				if TICDelete(" ".join(c)):
					await msg.delete()
					c.remove(DELETE)
				Even = True if testInContent(" ".join(c), EVEN) else False
				Odd = True if testInContent(" ".join(c), ODD) else False
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
			await msg.channel.send(res)

		elif cmd == "rolecount":
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
			m = findMember(c, msg)
			if m:
				roles = [x.mention for x in m.roles]
				roleCount = len(roles) - 1
				if Showroles:
					embed = discord.Embed(title=f"{m.name}'s Roles")
					embed.add_field(name="Count", value=roleCount)
					embed.add_field(name="Roles", value="".join(roles))
					await msg.channel.send(embed=embed)
				else: await msg.channel.send(roleCount)			
				return
			else: await msg.channel.send("User not found")

		elif cmd == "ship":
			if random.random() >= .985: await msg.channel.send("DISCLAIMER: I DO NOT SUPPORT SHIPPING PEOPLE IN ANY WAY, HOWEVER MY MASTER SEEMS TO HAVE OTHER PLANS")
			name1 = splitContent(content, ", ")[0].replace("[" + cmd + " ", "")
			name2 = splitContent(content, ", ")[1]
			await msg.channel.send(f'{name1[0:len(name1) // 2]}{name2[len(name2) // 2:]}')

		elif cmd in ["comproles", "compareroles"]:
			embed = discord.Embed(name="Role Comparison")
			c = content.split(PREFIX + testInContent(content, "comproles", "compareroles"))[1].split(" ")
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

		elif cmd == "family":
			if TICDelete(content): await msg.delete()
			with open("family.txt", "r") as f: await msg.channel.send(f.read())

		elif cmd == "mballreply":
			mssg = content.split(f'{cmd} ')[1]
			if userHasRole(msg, "mballresponseadder"):
				with open("mballresponse.txt", "a") as f:
					f.write(mssg + "\n")
				await msg.channel.send("message added")				
				return ""
			else:
				await msg.channel.send("you don't have perms")

		elif cmd == "8brdel":
			reply = content.split(f"{cmd} ")[1]
			if userHasRole(msg, "mballresponseadder"):
				with open("mballresponse.txt", "r+") as f:
					replies = f.read().split("\n")
					if reply in replies:
						replies.remove(reply)
						clearFile(f)
						f.write("\n".join(replies))
						await msg.channel.send(f'removed message: {reply}')
					else:
						await msg.channel.send("not a message")
			else:
				await msg.channel.send("you don't have perms")

		elif cmd == "count":
			await msg.delete()
			channel = discord.utils.get(msg.guild.channels, name="counting")
			highest = max([x.content.strip(".") async for x in channel.history(limit=5)])
			async for x in channel.history(limit=1):
				if isBot(x, client): return ""
			if testInContent(content, "--i"):
				await channel.send(f'*.{int(highest) + 1}.*')
				return ""
			elif testInContent(content, "--b"):
				await channel.send(f'**.{int(highest) + 1}.**')
				return ""
			elif testInContent(content, "--ib"):
				await channel.send(f'***.{int(highest) + 1}.***')
				return ""
			elif testInContent(content, "--e"):
				if testInContent(content, "-c"):
					color = splitContent(content, "-c ")[1]
					color.strip("#")
					print(hex(int(f'0x{color}', 16)))
				else: color = 0x000000
				await channel.send(embed=discord.Embed(title=f'.{int(highest) + 1}.', color=color))
				return 
			await channel.send(f'.{int(highest) + 1}.')

		elif cmd == "choose":
			options = splitContent(content, f'{cmd} ')[1].split(", ")
			PICKS = "-picks "
			picks = 1
			for op in options:
				if PICKS in op.lower():
					picks = int(op.split(PICKS)[1])
					options[options.index(op)] = op.split(PICKS)[0]
					break
			choices = [random.choice(options) for _ in range(int(picks))]
			await msg.channel.send("\n".join(choices))

		elif cmd in ["mballreplylist", "8ballreplylist", "8breplylist", "8brlist"]:
			if TICDelete(content): await msg.delete()
			with open("mballresponse.txt", "rb") as f:
				await msg.channel.send(file=discord.File(f, "mballresponse.txt"))

		elif cmd == "reverse":
			c = content
			if TICDelete(content): 
				await msg.delete()
				c = splitContent(content, DELETE)[0]
			await msg.channel.send(splitContent(c, f"{cmd} ")[1][::-1])

		elif cmd in ["piglatin", "igpayatinlay"]:
			CASE = "--kc"
			if testInContent(content, CASE):
				content = content.replace(CASE, "")
			else: content = content.lower()

			m = splitContent(content, cmd)[1].split(" ")
			m.pop(0)

			if TICDelete(" ".join(m)):
				await msg.delete()
				m = " ".join(m).replace(DELETE, "").split(" ")
				
			m = [x for x in m if x]
			for n, word in enumerate(m):
				if word[0] in "aeiou": m[n] += "ay"
				else:
					moveToEnd = [None if letter in "aeiou" else letter for letter in word]
					moveToEnd = moveToEnd[:moveToEnd.index(None)]		
					m[n] = f'{word[len(moveToEnd):]}{"".join(moveToEnd)}ay'
			await msg.channel.send(" ".join(m))

		elif cmd == "mostroles":
			if Stop: Stop = False
			c = content.split(PREFIX + cmd)[1]
			TOP = "-top "
			top = int(c.split(TOP)[1]) if TOP in c else 5
			if TICDelete(content): await msg.delete()

			memberRoles = {member.display_name.split("#")[0]: len(member.roles) - 1 for member in msg.guild.members}

			sortedKeys = sorted(memberRoles, key=memberRoles.get, reverse=True)
			top = [f'{r}, {memberRoles[r]}' for n, r in enumerate(sortedKeys) if n < top]
			await msg.channel.send("\n".join(top))

		elif cmd == "imscared":
			if TICDelete(content): await msg.delete()
			await msg.channel.send(random.choice(["don't be :smiling_imp:", "oh it's ok :)))))))))))))))))", "just don't pay attention of the sounds coming from your attic.....\nit's ok", "it's ok... he's comming :)"]))

		elif cmd == "spamdms":
			if TICDelete(content):
				await msg.delete()
				content = content.replace(DELETE, "")
			amnt = content.split(" ")[1]
			message = content[content.find(amnt):]
			message = message.replace(amnt, "")
			if not isInt(amnt):
				await msg.author.send("not a valid number")
				return ""
			amnt = int(amnt)
			for x in range(int(amnt)):
				if Stop:
					await msg.author.send("stopped")
					return ""
				await msg.author.send(message)
				await asyncio.sleep(random.uniform(.6, 1.3))		

		elif cmd == "clear":
			amnt = int(content.split(PREFIX + cmd)[1].strip())
			if userHasRole(msg, "Staff", "Supreme Admin :)", "Admin"):
				await msg.channel.purge(limit=amnt)
			else:
				await msg.channel.send(f"{msg.author.mention} you can't do that")
				await spam(msg, random.randint(10, 15), ["you cannot do that, don't do it again"], BlockStop=True)

		elif cmd == "color":
			c = splitContent(content, f'{cmd}')[1].strip()
			if TICDelete(content):
				await msg.delete()
				c = c.replace(DELETE, "")
			if ", " in c:
				color = [int(x) for x in c.split(", ")]
				hexColor = [str(hex(x))[2:] for x in color]
				await msg.channel.send(embed=discord.Embed(title=f'#{"".join(hexColor)}', color=discord.Color.from_rgb(color[0], color[1], color[2])))			
				return ""
			if not c: c = str(msg.author.top_role)
			m = discord.utils.find(lambda r: r.name.lower() == c.lower(), msg.guild.roles)
			if m:
				embed = discord.Embed(title=str(m.color), color=m.color)
				await msg.channel.send(embed=embed)					
			else: await msg.channel.send("not a valid role")

		elif cmd == "servericon":
			if TICDelete(content):	await msg.delete()
			embed = discord.Embed(title="Server icon", color=discord.Colour.from_rgb(180, 70, 180))
			embed.set_image(url=msg.guild.icon_url)
			await msg.channel.send(embed=embed)

		elif cmd in ["cc", "channelcreated"]:
			if splitContent(content, cmd)[1]:
				c = content.split(cmd)[1].strip()[2:-1]
				channel = discord.utils.get(msg.guild.channels, id=int(c))
				await msg.channel.send(channel.created_at)
				return ""
			await msg.channel.send(msg.channel.created_at)

		elif cmd == "pincount":
			if TICDelete(content): await msg.delete()
			channel = msg.channel
			if splitContent(content, cmd)[1]:
				c = content.split(cmd)[1].strip()[2:-1]
				channel = discord.utils.get(msg.guild.channels, id=int(c))
			pins = await channel.pins()
			await msg.channel.send(len(pins))
			return ""

		elif cmd == "changes":
			if TICDelete(content): await msg.delete()
			Latest = False if testInContent(content, "--nlatest") else True
			ver = splitContent(content, "-v ")[1].strip() if testInContent(content, "-v ") else None
			with open("CHANGELOG.txt", "r") as f:
				if Latest:
					c = f.read().split("\n")
					c = c[:c.index("====================================================================")]
				elif ver:
					c = f.read().split("\n")
					for lineN, line in enumerate(c):
						if ver == line.split(" ")[0]:
							c = c[lineN:c.index("====================================================================", lineN)]
							break
					else:
						await msg.channel.send("did not find version")
						return ""
				
				else: c = None

			with open("CHANGELOG.txt", "rb") as f:
				if testInContent(content, "--dms"): await msg.author.send("\n".join(c)) if c else msg.author.send(file=discord.File(f, "changes.txt"))
				else: await msg.channel.send("\n".join(c)) if c else await msg.channel.send(file=discord.File(f, "changes.txt"))
			return
				
		elif cmd in ["wiki", "wikipedia"]:
			if TICDelete(content):
				await msg.delete()
				content = content.replace(" " + DELETE, "")
			search = splitContent(content, cmd + " ")[1]
			search = search.replace(" ", "_")
			await msg.channel.send(f'https://en.wikipedia.org/wiki/Special:Search?search={search}')

		elif cmd == "commandcount":
			if TICDelete(content): await msg.delete()
			with open("cmdslist.txt", "r") as f:
				cmds = len(f.read().split("\n")) - 2
			await msg.channel.send(cmds)

		elif cmd == "hex":
			content = splitContent(content, cmd + " ")[1]
			num = list(map(lambda n: int(n), content.split(", "))) if ", " in content else [int(content)]
			hexes = list(map(lambda n: str(hex(n)).replace("0x", ""), num))
			await msg.channel.send(", ".join(hexes))

		elif cmd == "bin":
			content = splitContent(content, cmd + " ")[1]			
			num = list(map(lambda n: int(n), content.split(", "))) if ", " in content else [int(content)]
			bins = list(map(lambda n: str(bin(n)).replace("0b", ""), num))
			await msg.channel.send(", ".join(bins))

		elif cmd == "tof":
			cel = splitContent(content, cmd + " ")[1]
			await msg.channel.send("NaN") if not isInt(cel) else await msg.channel.send(9 / 5 * int(cel) + 32) #sends NaN if cel isn't a number otherwise sends feranheight

		elif cmd == "toc":
			fer = splitContent(content, cmd + " ")[1]
			await msg.channel.send("NaN") if not isInt(fer) else await msg.channel.send((int(fer) - 32) * 5/9) #same as above but reversed

		elif cmd == "response":
			if Stop: Stop = False
			if isBot(msg, client): return ""
			limit = 1000
			mssg = splitContent(content, "response ")[1]
			if testInContent(mssg, "-lim"):
				limit = int(splitContent(mssg, "-lim ")[1].strip())
				if limit > 100000:
					await msg.channel.send("you cannot go above 100k")
					return
				mssg = splitContent(mssg, " -lim")[0]
			async with msg.channel.typing():
				hist = [m.content async for m in msg.channel.history(limit=limit)]
				responses = []
				for n, message in enumerate(hist):
					if Stop: await msg.channel.send("stopped searching")
					if message == mssg: responses.append(hist[n - 1])
				if responses:
					await msg.channel.send(f'{msg.author.mention} I HAVE FOUND A RESPONSE\n{random.choice(responses)}')
				else: await msg.channel.send(f'did not find {mssg} in the past {limit} messages in this channel')

		#ongoing events
		elif cmd == "timer":
			if TICDelete(content):
				await msg.delete()
			if not runningTimer.get(msg.author.id):
				runningTimer[msg.author.id] = time.time()
				await msg.channel.send(f'{msg.author.mention} timer started')
				return
			if runningTimer.get(msg.author.id) and testInContent(content, "--get"):
				await msg.channel.send(embed=discord.Embed(title=str(round(time.time() - runningTimer[msg.author.id], 2)) + " seconds"))
			elif runningTimer.get(msg.author.id):
				await msg.channel.send(embed=discord.Embed(title=str(round(time.time() - runningTimer[msg.author.id], 2)) + " seconds"))
				del runningTimer[msg.author.id]
				return

		elif cmd == "guessinggame":
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
			playingGuessingGame[msg.author] = {"ans": ans, "lives": lives}
			return ""

		elif cmd == "reactiontime":
			await msg.channel.send("i will say GO and you have to send something as fast as possible (probably prepare the message before hand)")
			reacting[msg.author.id] = 0
			await asyncio.sleep(random.uniform(1.5, 6))
			reacting[msg.author.id] = time.time()
			await msg.channel.send("GO")
			return

		else: await msg.channel.send(f"that is not a {random.choice(['function', 'thing'])}")

	if reacting.get(msg.author.id):
		await msg.channel.send(f'{msg.author.mention} your reacion time is {time.time() - reacting[msg.author.id] - client.latency} seconds')
		del reacting[msg.author.id]

	if playingGuessingGame.get(msg.author):
		c = msg.content
		ans = playingGuessingGame[msg.author]["ans"]
		lives = playingGuessingGame[msg.author]["lives"]
		if c in ["stop", "giveup", "cancel"]:
			await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(100, 0, 0)))
			playingGuessingGame.pop(msg.author)
			return ""
		L = testInContent(c, "--lives+", "--lives-")
		if L: 
			lives += 1 if L == "--lives+" else -1
			c = c.replace(L, "")
		if isInt(c):
			lives -= 1
			if lives <= 0:
				if int(content) == ans:
					await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} ITS A DRAW', color=discord.Color.from_rgb(155, 155, 155)))
				else: await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(255, 0, 0)))
				playingGuessingGame.pop(msg.author)
				return ""
			elif int(content) == ans:
				await msg.channel.send(embed=discord.Embed(title=f"{msg.author.display_name} YOU WIN\nWITH {lives} LIVES LEFT", color=discord.Color.from_rgb(0, 255, 0)))
				playingGuessingGame.pop(msg.author)
				return ""
			await msg.channel.send("too high" if int(c) > ans else "too low")
		else: await msg.channel.send("NaN")
		playingGuessingGame[msg.author]["lives"] = lives
		await msg.channel.send(f"guess\nyou have {lives} lives left")

@client.event
async def on_voice_state_update(member, before, after):
	if not before.channel and after.channel:
		role = discord.utils.get(member.guild.roles, name="vc")
		await member.add_roles(role)
	elif before.channel and not after.channel:
		role = discord.utils.get(member.guild.roles, name="vc")
		await member.remove_roles(role)

client.run(token)