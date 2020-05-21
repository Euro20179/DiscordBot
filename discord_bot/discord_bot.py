import discord
from discord.ext import commands
import time, datetime
import random
import string
import pyautogui
import wikipedia
import asyncio

#make helpmsg a json file with categories and stuff

DELETE = "--delete"
VERSION = "2.2.1"
Stop = False

playingGuessingGame = {}
runningTimer = {}
reacting = {}

PREFIX = "["

token = "NjQxNzk1NjU2Mzc3MTcyMDAw.XcNk8g.HEvnaXjuXFQhN1iilaaffbiPcoo"

client = commands.Bot(command_prefix=PREFIX)

def isBot(msg, client):
	if msg.author == client.user: return True
	if msg.author.bot: return True
	return False

def testInContent(content, *testfor):
	for x in testfor:
		if x.lower() in content.lower():
			return x
	return ""
	
def TICDelete(content):
	return testInContent(content, DELETE)

def getCmd(content):
	return content.split(" ")[0][1:]

def splitContent(content, *split):
	for x in split:
		if x in content:
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
	for x in role:
		if discord.utils.get(msg.author.roles, name=x):
			return True
	return False

def isInt(testee):
	try:
		int(testee)
		return True
	except:	return False

def findMember(c, msg):
	return discord.utils.find(lambda m: str(m.id) == c or str(m.display_name.split("#")[0].lower()) == c.lower(), msg.guild.members)

async def spam(msg, messages, message):
	global Stop
	for _ in range(int(messages)):
		if Stop:
			await msg.channel.send(stop("stopped spam", "Stopped spam"))						
			return ""
		await msg.channel.send(random.choice(message))
		await asyncio.sleep(random.uniform(.6, 1.3))

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game("I watch very closely"))
	print(f"ONLINE\nversion: {VERSION}")

@client.event
async def on_message(msg):
	global Stop, playingGuessingGame
	content = msg.content

	if msg.author.id == 311621977339068418 and msg.channel.id not in (658815060646297659, 476977066839900165):
		await msg.delete()
		print("message deleted")

	if not content:
		return

	if random.random() >= .998: 
		if isBot(msg, client): return
		await msg.channel.send(random.choice(["mhm", "interesting", "fascinating"]))
		
	if content == f'is <@!{client.user.id}> a bot' or content == f'are you a bot <@!{client.user.id}>':
		await msg.channel.send("no <:Watching1:697677860336304178>")
	if f"<@!{client.user.id}>" in content:
		await msg.channel.send("<:Watching1:697677860336304178>")

	if content[0] == PREFIX:

		cmd = getCmd(content)

		if cmd == "ENDPLS" and msg.author.id == 334538784043696130:
			await msg.channel.send("Logging out")
			await client.logout()

		if cmd == "help":
			if TICDelete(content): await msg.delete()
			if testInContent(content, "--indepth"):
				with open("helpMsg.txt", "rb") as f:
					await msg.channel.send(file=discord.File(f, "helpMsg.txt"))
			else:
				with open("cmdslist.txt", "r") as f:
					await msg.channel.send(embed=discord.Embed(title="help", description=f.read(), color=discord.Color(0x00ffe2)))

		elif cmd == "ping":
			if splitContent(content, "ping")[1]:
				await msg.channel.send("are you trying to ping someone..... don't do that. :/")
				return ""
			if TICDelete(content): await msg.delete()
			if random.random() >= .99:
				await msg.channel.send("uh yeah tbh i don't really know what this does, like i have an idea but like idk")
			elif random.random() >= .97:
				await msg.channel.send("LOL GET PRANKD THIS DOES NOTHING ROFL XD XD XD XD XD")
			else:
				await msg.channel.send(f':ping_pong: {round(client.latency * 1000)}ms')	

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
			else:
				await msg.channel.send(f'Answer: {random.choice(responses)}')

		elif cmd == "spam":
			if Stop: Stop = False
			if isBot(msg, client): return ""

			c = splitContent(content, f"{cmd} ")[1]

			if TICDelete(c):
				await msg.delete()
				c = c.replace(DELETE, "")

			messages = c[:c.find(" ")]

			if not isInt(messages):
				await msg.channel.send("not a valid number of messages")			
				return ""
			lim = random.randint(30000, 100000)
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
			if random.random() >= .5:
				await msg.channel.send(f'{random.choice(EYES)}{random.choice(MOUTHS)}')				
				return ""
			await msg.channel.send(f'{random.choice(MOUTHS)}{random.choice(EYES)}')

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
			if content.lower().split(" ")[1].isdigit():
				amount = int(content.lower().split(" ")[1])

			if TICDelete(content): await msg.delete()

			chars = []
			for x in range(amount):
				char = random.randint(0, 185000)
				if "--value" in content:
					chars.append(f'{chr(char)} value: ({char})')
				else:
					chars.append(chr(char))

			await msg.channel.send("\n".join(chars))
	
		elif cmd == "serveremote":
			try:
				amount = int(content.lower().split(" ")[1])
			except:
				amount = 1

			if TICDelete(content): await msg.delete()

			EMOTES = client.emojis

			sendE = [random.choice(EMOTES) for _ in range(amount)]

			await msg.channel.send("\n".join(sendE))

		elif cmd == "doesnothing":
			filename = splitContent(content.lower(), cmd)[1]
			if TICDelete(filename):
				filename = filename.replace(DELETE, "")
				await msg.delete()

			with open(f".\\roles\\{filename}.txt", "w") as f:
				for x in client.get_all_members():
					try:
						f.write("\n")
						f.write(str(x))
					except:
						f.write(f"UNWRITEABLE")
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

			with open(f'.\\roles\\{filename}.txt', "rb") as f:
				await msg.channel.send(file=discord.File(f, f'{filename}.txt'))

		elif cmd == "spacer":
			c = splitContent(content.lower(), f'{cmd} ')[1]
			spaces = c[:c.find(" ")]
			c = c[c.find(" "):]
			if not isInt(spaces):
				await msg.channel.send(f"{spaces} is not a valid number of spaces")
				return
			await msg.delete()
			spaces = int(spaces)
			add = " " * spaces
			word = add.join(c)
			await msg.channel.send(word)

		elif cmd == "version":
			if TICDelete(content): await msg.delete()
			await msg.channel.send(VERSION)

		elif cmd in ["upperlower", "ul"]:
			mssg = " ".join(content.lower().split(PREFIX + f"{cmd} ")[1::])
			if not TICDelete(mssg):
				await msg.delete()
			else:
				mssg = mssg.replace(DELETE, "")

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
			time = 15
			if testInContent(content, "-time"):
				time = int(splitContent(content, "-time ")[1].strip())
			user1 = await client.fetch_user(msg.author.id)
			user2 = await client.fetch_user(splitContent(content, " ")[1][3:-1])
			if user2 == client.user.id:
				await msg.channel.send(f"sorry {user1.mention} you have to face a real player")
			await user1.send(f"say your move here, you have {time} seconds (typos will mess up results)")
			await user2.send(f"say your move here, you have {time} seconds (typos will mess up results)")
			await asyncio.sleep(time)
			async for rep in user1.dm_channel.history(limit=1):
				resp1 = rep.content.lower()
			async for rep in user2.dm_channel.history(limit=1):
				resp2 = rep.content.lower()
			await msg.channel.send(f'{user1.mention} said {resp1}\n{user2.mention} said {resp2}')

			opps = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

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
			if TICDelete(content): msg.message.delete()
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
			RType = testInContent(c, "-round ", "-r ")
			if RType:
				r = int(content.split(RType)[1].split(" ")[0])
				c = c.split(RType)[0]
			else: r = 3
			san = round(random.uniform(-1.5, 101), r)

			cases = {san > 100: f'{c} is so sane that they have become the universe itself',
					 san >=49.5 and san <= 50.5: f'{c} is perfectly balanced between sane and insane',
					 san < 0: f'how is {c} even alive'}
					 
			for case in cases.keys():
				if case:
					await msg.channel.send(cases[case])
					break
			else:
				await msg.channel.send(f'{c} has {san}% sanity')

		elif cmd == "coin":
			if TICDelete(content): 
				await msg.delete()
				content = content.replace(DELETE, "")
			res = "heads" if random.random() >= .5 else "tails"
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
				title = res
			
			embed = discord.Embed(title=title, color=color)
			await msg.channel.send(embed=embed)

		elif cmd == "rand":
			if Stop:
				Stop = False
			c = content.split(PREFIX + "rand")[1].split(" ")
			c.pop(0)
			EVEN = "--even"
			ODD = "--odd"
			if TICDelete(" ".join(c)):
				await msg.delete()
				c.remove(DELETE)
			if testInContent(" ".join(c), EVEN):
				Even = True
				c.remove(EVEN)
			else:
				Even = False
			if testInContent(" ".join(c), ODD):
				Odd = True
				c.remove(ODD)
			else:
				Odd = False
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
					if Stop:
						await msg.channel.send(stop("stopped picking a number"))
					res = random.randint(int(low), int(high))
					if Even and res % 2 != 0:
						continue					
					if Odd and res % 2 == 0:
						continue
					else:
						break
			else:
				res = random.uniform(float(low), float(high))
				if r:
					res = round(res, r)
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
			with open("family.txt", "r") as f:
				await msg.channel.send(f.read())

		elif cmd == "mballreply":
			mssg = content.split(f'{cmd} ')[1]
			if userHasRole(msg, "mballresponseadder"):
				with open("mballresponse.txt", "a") as f:
					f.write(mssg + "\n")
				await msg.channel.send("message added")				
				return ""
			else:
				await msg.send("you don't have perms")

		elif cmd == "8brdel":
			reply = content.split(f"{cmd} ")[1]
			if userHasRole(msg, "mballresponseadder"):
				with open("mballresponse.txt", "r+") as f:
					replies = f.read().split("\n")
					if reply in replies:
						replies.remove(reply)
						f.seek(0)
						f.truncate()
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
			if testInContent(content, "--i"):
				await channel.send(f'*.{int(highest) + 1}.*')
				return ""
			elif testInContent(content, "--b"):
				await channel.send(f'**.{int(highest) + 1}.**')
				return ""
			elif testInContent(content, "--ib"):
				await channel.send(f'***.{int(highest) + 1}.***')
				return ""
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
			else:
				content = content.lower()

			m = splitContent(content, "piglatin", "igpayatinlay")[1].split(" ")
			m.pop(0)

			if TICDelete(" ".join(m)):
				await msg.delete()
				m = " ".join(m).replace(DELETE, "").split(" ")
				
			m = [x for x in m if x]
			CONSONANT = [a for a in string.ascii_letters if a not in ["a", "e", "i", "o", "u", "y"]]
			for n, word in enumerate(m):
				if word[0] in "aeiou":
					m[n] += "ay"
				else:
					moveToEnd = []
					for letter in word:
						if letter.lower() in CONSONANT:
							moveToEnd.append(letter)
						else:
							break
					m[n] = word[len(moveToEnd):] + "".join(moveToEnd) + "ay"
			await msg.channel.send(" ".join(m))
		elif cmd == "mostroles":
			if Stop: Stop = False
			c = content.split(PREFIX + cmd)[1]
			TOP = "-top "
			top = int(c.split(TOP)[1]) if TOP in c else 5
			if TICDelete(content): await msg.delete()

			memberRoles = {member.display_name.split("#")[0]: len(member.roles) - 1 for member in msg.guild.members}

			sortedKeys = sorted(memberRoles, key=memberRoles.get, reverse=True)
			for n, r in enumerate(sortedKeys):
				if Stop:
					stop()
					break
				if n >= top:
					break
				await msg.channel.send(f'{r}, {memberRoles[r]}')

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
				for x in range(random.randint(10, 15)):
					await msg.author.send("you cannot do that, don't do it again")
					await asyncio.sleep(random.uniform(.6, 1.3))

		elif cmd == "color":
			c = splitContent(content, f'{cmd}')[1].strip()
			if TICDelete(content):
				await msg.delete()
				c = c.replace(DELETE, "")
			if ", " in c:
				color = [x for x in c.split(", ")]
				await msg.channel.send(embed=discord.Embed(title=", ".join(color), color=discord.Color.from_rgb(int(color[0]), int(color[1]), int(color[2]))))			
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

		elif cmd in ["cc"]:
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
			if testInContent("--chat"):
				with open("CHANGELOG.txt", "rb") as f:
					await msg.channel.send(file=discord.File(f, "changes.txt"))
				return
			else:
				with open("CHANGELOG.txt", "rb") as f:
					await msg.author.send(file=discord.File(f, "changes.txt"))
				return
				
		elif cmd == "commandcount":
			if TICDelete(content): await msg.delete()
			with open("cmdslist.txt", "r") as f:
				cmds = len(f.read().split("\n")) - 2
			await msg.channel.send(cmds)

		elif cmd == "response":
			if isBot(msg, client):
				return ""
			limit = 1000
			mssg = splitContent(content, "response ")[1]
			if testInContent(mssg, "-lim"):
				limit = int(splitContent(mssg, "-lim ")[1].strip())
				if limit > 100000:
					await msg.channel.send("you cannot go above 100k")
				mssg = splitContent(mssg, " -lim")[0]
			async with msg.channel.typing():
				hist = [m.content async for m in msg.channel.history(limit=limit)]
				for n, message in enumerate(hist):
					if message == mssg:
						await msg.channel.send(f'{msg.author.mention} I HAVE FOUND A RESPONSE\n{hist[n - 1]}')
						break
				else:
					await msg.channel.send(f'did not find {mssg} in the past {limit} messages in this channel')


		#ongoing events
		elif cmd == "timer":
			if TICDelete(content):
				await msg.delete()
			if not runningTimer.get(msg.author):
				runningTimer[msg.author] = time.time()
				await msg.channel.send(f'{msg.author.mention} timer started')
				return
			if runningTimer.get(msg.author):
				await msg.channel.send(embed=discord.Embed(title=str(round(time.time() - runningTimer[msg.author], 2)) + "seconds"))
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
			reacting[msg.author] = 0
			await asyncio.sleep(random.uniform(1, 6))
			reacting[msg.author] = time.time()
			await msg.channel.send("GO")
			return


		else: await msg.channel.send(f"that is not a {random.choice(['function', 'thing'])}")

	if reacting.get(msg.author):
		await msg.channel.send(f'{msg.author.mention} your reacion time is {time.time() - reacting[msg.author] - client.latency} milliseconds')
		del reacting[msg.author]


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
		if c:
			lives -= 1
			if lives <= 0 and int(content) == ans:
				await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} ITS A DRAW', color=discord.Color.from_rgb(155, 155, 155)))
				playingGuessingGame.pop(msg.author)
				return ""
			elif lives <= 0:
				await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(255, 0, 0)))
				playingGuessingGame.pop(msg.author)
				return ""
			elif int(content) == ans:
				await msg.channel.send(embed=discord.Embed(title=f"{msg.author.display_name} YOU WIN\nWITH {lives} LIVES LEFT", color=discord.Color.from_rgb(0, 255, 0)))
				playingGuessingGame.pop(msg.author)
				return ""

			send = "too high" if int(c) > ans else "too low"
			await msg.channel.send(send)
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