from common import *

class FileException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

async def stop(*args, **kwargs)->None: #similar to how raise StopIteration works, it stops whatever is happening
    global Stop
    Stop = True
    if args: return random.choice(args)

async def hlp(msg, content, cmd="help"):
    global CATS, CMDLIST, CUSTOMCMDS
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    c = Content(content)
    added = False
    Raw = True if c @ "--raw" else False
    File = True if c @ "--file" else False
    for op, param in c.opsWithParams():
        if op == "-added":
            added = param
    cat = str(c).upper()
    if added:
        with open(f'cmds.json', "r") as f:
            data = json.load(f)
            cmds = [cmd["name"] for cat in data for cmd in cat["cmds"] if cmd.get("date") == added]
            return await msg.channel.send("\n".join(cmds))
    if not cat:
        embed = discord.Embed(title="General", color=discord.Color(0x0000ff))
        with open("cmds.json", "r") as j:
            data = json.load(j)
            for cat in data:
                embed.add_field(name=cat["cat"], value=cat["desc"])
        await msg.channel.send(embed=embed)
        return await embedToReadableDict(msg, embed)
    elif cat in CATS:
        embed = discord.Embed(title=cat, color=discord.Color(0x00ffe2))
        if cat == "CUSTOM":
            for cmd in CATS[cat]:
                embed.add_field(name=f'{cmd["name"]}', value=f'``{cmd["name"]}``  {cmd["desc"]}')
        else:
            for cmd in CATS[cat]:
                embed.add_field(name=f'{cmd["name"]}', value=f'``{cmd["desc"]}``', inline=False)
        try:
            if File: raise Exception("wanted file")
            msg = await msg.channel.send(embed=embed)
            return await embedToReadableDict(msg, embed)
        except:
            if not cat: cat = "help"
            with open(f'{cat}.txt', "w") as f:
                for cmd in CATS[cat]:
                    f.write(f'{cmd["name"]}\n\nparams: {cmd["params"]}\n\nDescription: {cmd["desc"]}\n\nAliases: {cmd.get("aliases")}\n\nAdded: {cmd.get("date")}\n\n\n\n')
            with open(f'{cat}.txt', "rb") as f:
                await msg.channel.send(file=discord.File(f, f'{cat}.txt'))
            os.remove(f"{cat}.txt")
        return cat

    with open("cmds.json", "rb") as j:
        if Raw: #the file
            await msg.channel.send(file=discord.File(j, "cmds.json"))
        else: #by specific commoand
            command = splitContent(content, " ", index=1)
            embed = discord.Embed(title=command, color=discord.Color(0x00ffe2))
            for cmd in CATS.values():
                for c in cmd:
                    al = c.get("aliases")
                    if al:
                        if command in al: isCmd = True
                    else: isCmd = False
                    if c["name"] == command or isCmd:
                        params = c["params"]
                        desc = c["desc"]
                        aliases = c.get("aliases")
                        date = c.get("date")
                        Locked = c.get("Locked")
                        addedBy = c.get("addedby")
                        editedBy = c.get("editedby")
                        if aliases: aliases = ",\n".join(f'``{x}``' for x in aliases)
                        break
            try: 
                if params: embed.add_field(name="params", value=f'``{params}``', inline=False)
                embed.add_field(name="description", value=f'``{desc}``', inline=False)
                if aliases: embed.add_field(name="aliases", value=aliases, inline=False)
                if Locked is not None: embed.add_field(name="locked", value=Locked, inline=False)
                if addedBy is not None: embed.add_field(name="added by", value=(await client.fetch_user(int(addedBy))).name, inline=False)
                if editedBy: embed.add_field(name="edited by", value="\n".join([(await client.fetch_user(int(userId))).name for userId in editedBy]), inline=False)
                embed.add_field(name="date added", value=date if date else "unknown", inline=False)
            except Exception as e: 
                print(e)
                return await msg.channel.send('command not found')
            msg = await msg.channel.send(embed=embed)
            return await embedToReadableDict(msg, embed)

async def spam(msg, messages, message, BlockStop=False):
    global Stop
    for i in range(int(messages)):
        if Stop and not BlockStop:
            Stop = False
            return await msg.channel.send(await stop("Stopped"))
        msg = await msg.channel.send(random.choice(message).replace("{count}", str(i + 1)).replace("{rcount}", str(int(messages) - i)))
        await asyncio.sleep(random.uniform(.7, 1.3))
    return msg

async def ping(msg, content, cmd="ping"):
    startFunction = time.time()
    if random.random() >= .95:
        await msg.author.send("upupdowndownleftrightleftright")
        await asyncio.sleep(5)
        await msg.author.send("OH SHOOT I WASNT SUPPOSED TO SAY TH-")
        await asyncio.sleep(1)
        await msg.author.send("goodbye")

    elif random.random() >= .97:
        return await msg.channel.send("LOL GET PRANKD THIS DOES NOTHING ROFL XD XD XD XD XD")
    else: 
        start = time.time()
        mssg = await msg.channel.send(f'Ping to discord: ``{(client.latency * 1000)}`` ms')	
        end = time.time()
        startEdit = time.time()
        await mssg.edit(content=mssg.content + f'\nMessage send time: ``{(end - start) * 1000}`` ms')
        endEdit = time.time()
        await mssg.edit(content=mssg.content + f'\nMessage edit time: ``{(endEdit - startEdit) * 1000}`` ms')
        await mssg.edit(content=mssg.content + f'\nTotal execute time ``{(time.time() - startFunction) * 1000}`` ms')
        return mssg

async def echo(msg, content, cmd="echo"):
    c = Content(content)
    c.formatMessage(msg, {"{echo}": Content(content.replace(" {echo} ", "").replace(" {echo}", "").replace("{echo} ", "").replace("{echo}", ""))})
    if not c @ "--nodel":
        try: await msg.delete()
        except: pass
    for op, param in c.opsWithParams({"test": (..., '"')}):
        if op == "-e":
            if param: color = int(param, 16)
            else: color = 0x000000
            embed = discord.Embed(title=str(c), color=discord.Color(color))
            await msg.channel.send(embed=embed)			
            return await embedToReadableDict(msg, embed)
        if op == "-wait":
            try: await asyncio.sleep(float(param))
            except: return await msg.channel.send("-wait must be float")
    if random.random() > .99: await msg.author.send("the secret message dm euro for a doubley secret role, if you tell anyone how you got this the role will be taken away\nif you already have the role, you may choose to dm a screenshot of this message to someone, and they have the chance to get the role")	
    return await msg.channel.send(str(c), tts=True if c @ "--tts" else False)

async def timers(msg, content, cmd="timers"):
    embed = discord.Embed(title="Timers")
    with open(timersPath, "r") as tJ:
        data = json.load(tJ)
        for user, t in data.items():
            embed.add_field(name=user, value=round(time.time() - t, 2))
        msg = await msg.channel.send(embed=embed)
        return await embedToReadableDict(msg, embed)

async def levelMessage(msg, content, cmd="lvlmsg"):
    if isBot(msg, client): return await msg.channel.send("easter e g g")
    changeTo = Content(content)
    yn=Yes = changeTo @ "--y"
    with open(levelingDataFilePath, "r+") as j:
        data = json.load(j)
        userData = data[str(msg.author.id)]
        if changeTo.testOps("--see", "--get", "--s", "--g"):
            content = Content(userData["message"], removeCmd=False)
            content.formatMessage(msg, {"{level}": userData['level'], "{xp}": userData["xp"]}, removeCmd=False)
            return await msg.channel.send(str(content))
        if not Yes:
            await msg.channel.send("type y to change message, type n to cancel")
            try: yn = (await client.wait_for('message', check=lambda message: message.author == msg.author, timeout=60.0)).content.lower()
            except asyncio.TimeoutError: yn = "n"
        if yn in ("yes", "y") or Yes:
            userData["message"] = str(changeTo)
            clearFile(j)
            json.dump(data, j)
            return await msg.channel.send(f"changed to {changeTo}")
        return await msg.channel.send("CANCELLED")

async def cmdUsage(msg, content, cmd="commandusage"):
    content = Content(content)
    top = 10
    for op in content.opsWithParams():
        if "-top" == op[0]:
            top = int(op[1])
    if content @ "--raw":
        with open(commandusageFilePath, "rb") as j:
            return await msg.channel.send(file=discord.File(j, commandusageFilePath))
    with open(commandusageFilePath, "r+") as j:
        data = json.load(j)
        if content and top == 10:
            commandUse = data.get(str(content))
            if not commandUse:
                return await msg.channel.send("command not found")
            embed = discord.Embed(title=str(content))
            embed.add_field(name="times", value=commandUse)
            await msg.channel.send(embed=embed)
            return await embedToReadableDict(msg, embed)
        else:
            data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=False if content.testOps("--least", "--ltg") else True)}
            send = "\n".join([f'{n + 1}: {c[0]}, {c[1]}' for n, c in enumerate(data.items()) if n < top])
            try:
                clearFile(j)
                json.dump(data, j) 
                return await msg.channel.send(send)
            except: return await msg.channel.send("too long of a message")
            

async def iq(msg, content, cmd="iq"):
    iq = random.randint(-3, 200)
    content = Content(content)
    c = msg.author.mention if not content.split(" ")[0] else str(content)
    await msg.channel.send(f'{c}\'s iq is *DRUMROLL*...')
    await asyncio.sleep(random.uniform(.7, 1.3))
    return await msg.channel.send({msg.author.bot: "i am computer i have [ERROR] iq",
            iq == 200: f'you are the next einstein, you are smart enough to realize iq is dumb, so there is no need to say it',
            iq > 150 and iq < 200: f"that's a pretty high iq: {iq}",
            iq > 50 and iq <= 150: iq,
            iq <= 50 and iq >= 0: f"you good there mate, your iq is {iq}",
            iq < 0: f"you literally don't have a brain you somehow have a negative iq idek\nIQ: {iq}"}.get(True))

async def shrug(msg, content, cmd="shrug"):
    msg = await msg.channel.send(content=r"¯\_(ツ)_/¯")
    await asyncio.sleep(.3)
    await msg.edit(content=r"¯\\-(ツ)-/¯")
    await asyncio.sleep(.3)
    await msg.edit(content=r"¯\_(ツ)_/¯")
    return msg

async def getUserData(user):
    with open(levelingDataFilePath, "r") as f:
        data = json.load(f)
        return data.get(str(user))

async def level(msg, content, cmd="level"):
    content = Content(content)
    user = content.getUser(msg)
    userData = await getUserData(user.id)
    with open(levelingDataFilePath, "r") as f:
        data = json.load(f)
        users = [(discord.utils.get(msg.guild.members, id=int(user.id)).id, int(data[userr]["level"])) for userr in data.keys()]
        users.sort(key=lambda x: x[1], reverse=True)
    level = userData["level"]
    xp = userData["xp"]
    required = userData["required"]
    message = userData["message"]
    pos = users.index((user.id, level)) + 1
    embed = discord.Embed(title=user.display_name, color=user.color)
    for k, i in userData.items():
        if k == "lastTalked": break
        embed.add_field(name=k, value=i)
    embed.add_field(name="rank #", value=pos)
    embed.add_field(name="xp needed", value=required - xp)
    embed.add_field(name="approx minutes", value=round((required - xp) / 57.5)) #TODO format this
    embed.add_field(name="level up mesage", value=str(Content(message, removeCmd=False).formatMessage(msg, kwargs={"{level}": level, "{xp}": xp}, removeCmd=False, ret=True)), inline=False)
    msg = await msg.channel.send(embed=embed)
    return await embedToReadableDict(msg, embed) 

async def leaderboard(msg, content, cmd="top"):
    content = Content(content)
    content.calcOps()
    if content @ "--raw":
        with open(levelingDataFilePath, "rb") as f:
            return await msg.channel.send(file=discord.File(f, levelingDataFilePath))
    top = 10
    if str(content):
        try: top = int(content)
        except: await msg.channel.send("NaN")
    with open(levelingDataFilePath, "r") as f:
        data = json.load(f)
        users = [(discord.utils.get(msg.guild.members, id=int(user)), int(data[user]["level"]), int(data[user]["xp"])) for user in data.keys()]
        users.sort(key=lambda x: (x[1] ** 10) + (x[2] / 1000), reverse=True)
        embed = discord.Embed(title=f"Top {top}", color=users[0][0].color)
        firstPlaceRole = discord.utils.get(msg.guild.roles, id=713979970287829033)
        for n, user in enumerate(users):
            if not user[0]: continue
            if firstPlaceRole in user[0].roles:
                await user[0].remove_roles(firstPlaceRole)
            if n > top - 1: break
            embed.add_field(name=str(n + 1), value=f'{user[0].mention}\nLevel: {user[1]}\nXp: {user[2]}')

        if firstPlaceRole not in users[0][0].roles:
            await users[0][0].add_roles(firstPlaceRole)
        await msg.channel.send(embed=embed)

async def magicBall(msg, content, cmd="8ball"):
    opOps = Content(content).opsWithParams()
    with open(mballresponseFilePath, "r") as f:
        responses = f.read().split("\n")
    for op, param in opOps:
        if op == "-e":
            return await msg.channel.send(embed=discord.Embed(title=random.choice(responses), color=int(param, 16) if param else 0x000000))
    return await msg.channel.send(random.choice(responses))

async def spamCmd(msg, content, cmd="spam"):
    global Stop
    if Stop: Stop = False
    c = Content(content)
    try: messages = int(c.split(" ")[0])
    except: return await msg.channel.send("not a valid number of messages")		

    lim = random.randint(40000, 110000)
    if messages > lim:
        return await msg.channel.send(f"pls consult a psychiatrist that's too many messages\nthe limit is: {lim}")		

    if messages < 0: return await msg.channel.send("ERROR: MESSAGE COUNT LESS THAN 0")

    if "-random" in c:
        c.replace("-random ", "")
        c = " ".join(c.split(" ")[1:])
        options = c.split("|")
        return await spam(msg, int(messages), options)

    message = " ".join(c.split(" ")[1:])
    await spam(msg, messages, [message])
    if random.random() >= .99: await msg.channel.send("You found an easter egg hehe")
    else: return await msg.channel.send(random.choice(("done", "Done")))

async def randomFace(msg, content, cmd="randomface"):
    BROWS = (">", "|")
    EYES = (":", ";")
    MOUTHS = (")", "(", "{", "}", "[", "]", "p", "P", "d", "l", "C", "c")
    if random.random() >= .995:
        return await msg.channel.send("()-()\n ___")
    if random.random() >= .8:
        return await oneLineCmd(msg, f'{random.choice(BROWS)}{random.choice(EYES)}{random.choice(MOUTHS)}')
    else: 
        return await oneLineCmd(msg, f'{random.choice(EYES)}{random.choice(MOUTHS)}')

async def alphabet(msg, content, cmd="alphabet"):
    send = string.ascii_lowercase
    content = Content(content)
    if content @ "--vowels": send = "aeiou(y)"
    if content @ "--consonants":
        send = "".join([x for x in string.ascii_lowercase if x not in "aeiou"])
    if random.random() > .98: send = send[::-1]
    return await msg.channel.send(send)

async def unicodeChar(msg, content, cmd="unicodechar"):
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-sep":
            try: sep = {r'\t': "\t", r"\n": "\n"}[param]
            except: sep = param
            break
    else: sep = "\n"
    try: amount = int(content)
    except: amount = 1
    return await msg.channel.send(sep.join([chr(random.randint(0, 185000)) for _ in range(amount)]))

async def serverEmote(msg, content, cmd="serveremote"):
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-sep":
            try: sep = {r'\t': "\t", r"\n": "\n"}[param]
            except: sep = param
            break
    else: sep = "\n"
    try: amount = int(content)
    except: amount = 1
    return await msg.channel.send(sep.join([str(random.choice(client.emojis)) for _ in range(amount)]))

async def writeRoles(msg, content, cmd="doesnothing"):
    filename = Content(content)
    with open(f".\\roles\\{filename}.txt", "w") as f:
        for x in client.get_all_members():
            try: f.write(f'\n{str(x.name)}\n')
            except: f.write(f"\n{x.id}\n")
            for y in x.roles:
                try: f.write(f'{y.name}\n')
                except: f.write(f'{y.id}\n')
    with open(f'.\\roles\\{filename}.txt', "rb") as f:
        await msg.channel.send(file=discord.File(f, f'{filename}.txt'))

async def spacer(msg, content, cmd="spacer"):
    try: await msg.delete()
    except: pass
    sep = " "
    content = Content(content)
    try: spaces = int(content.split(" ")[0])
    except: spaces = 1
    c = content.split(" ", pastIndex=1)
    if "-sep" in c:
        sep = content.split("-sep ")[1]
        c = c.split("-sep")[0]
        if sep == r"\n": sep = "\n"
        if sep == r"\t": sep = "\t"
    add = sep * int(spaces)
    word = add.join(c)
    return await oneLineCmd(msg, word)

async def upperLower(msg, content, cmd="upperlower"):
    mssg = content[len(cmd) + 2:]
    try: await msg.delete()
    except: pass

    newPhrase = []

    for val, letter in enumerate(mssg):
        if val > 0:
            if mssg[val - 1] != " " and newPhrase[val - 1].islower():
                letter = letter.upper()
            elif newPhrase[val - 2].islower() and mssg[val - 1] == " ":
                letter = letter.upper()
        newPhrase.append(letter)

    return await msg.channel.send("".join(newPhrase))

async def startRPS(msg, content, cmd="rps"):
    opps = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    setTo = {"r": "rock", "p": "paper", "s": "scissors"}
    t = 15
    if testInContent(content, "-time"):
        t = int(splitContent(content, "-time ", index=1).strip())
        if t >= 120: return await msg.channel.send("sorry must be shorter than 2 minutes or 120 seconds")
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
            if user2.mention != user1.mention: 
                await addMoney(user2, random.randint(1, 5))
                await addMoney(user1, random.randint(-5, -1))
            return await msg.channel.send(f'{user2.mention} WINS')
        elif opps[resp1] == resp2:
            if user2.mention != user1.mention: 
                await addMoney(user2, random.randint(-5, -1))
                await addMoney(user1, random.randint(1, 5))
            return await msg.channel.send(f'{user1.mention} WINS')
        else: await msg.channel.send("ITS A DRAW")
    else: await msg.channel.send("either someone spelled something wrong, or someone isn't playing by the rules")

async def complexMessage(msg, content, cmd="complexmessage"):
    content = Content(content).split("|")
    try: await msg.delete()
    except: pass
    try:
        send = content[0].strip().lower()
        filename = content[1]
        mssg = content[2]
    except: return await msg.channel.send("make sure you give and seperate each paremeter with a '|'")

    dm = (send == "dm")
    send = dm^True

    if cmd == "message": filename = f'{filename}.txt'

    with open(f'.\\message\\{filename}', "w") as f:
        f.write(mssg)
    with open(f'.\\message\\{filename}', 'rb') as f:
        if send: await msg.channel.send(file=discord.File(f, filename))
        if dm:await msg.author.send(file=discord.File(f, filename))

async def sanity(msg, content, cmd="sanity"):
    c = Content(content)
    if "-r" in c:
        r = int(c.split("-r ")[1])
        c = c.split("-r")[0]
    else: r = 2
    san = round(random.uniform(-1.5, 101), r)
    cases = {san > 100: f'{c} is so sane that they have become the universe itself',
                san >=49.5 and san <= 50.5: f'{c} is perfectly balanced between sane and insane',
                san < 0: f'how is {c} even alive'}            
    return await msg.channel.send(cases.get(True)) if cases.get(True) else await msg.channel.send(f'{c} has {san}% sanity')

async def coin(msg, content, cmd="coin"):
    title = res = "heads" if random.random() >= .5 else "tails"
    if " " in content:
        bet = content.split(" ")[1].strip()
        if bet == "t": bet = "tails"
        if bet == "h": bet = "heads"
        if not bet.isnumeric():
            color, title = (0x00ff00, "YOU WIN") if res == bet else (0xff0000, "YOU LOSE")
            add = random.randint(1, 3) if res == bet else random.randint(-3, -1)
            await addMoney(msg.author, add)
            title += f'\nYOU WON {add}' if res == bet else f'\nYOU LOSE {abs(add)}'
        else:
            results = {}
            for _ in range(int(bet)):
                while True:
                    f = random.random()
                    if f != .5: break
                flip = "heads" if f > .5 else "tails"
                try: results[flip] += 1
                except: results[flip] = 1
            embed = discord.Embed(title=f'Heads: {results["heads"]}\nTails: {results["tails"]}', color=0x00aa00)
            return await msg.channel.send(embed=embed)
    else:  color = 0xff00ff if res == "heads" else 0x0000ff
    embed = discord.Embed(title=title, color=color)
    await msg.channel.send(embed=embed)

async def weightedCoin(msg, content, cmd="weightedcoin"):
    content = Content(content).split(" ")
    headsOdds = content[0]
    if len(content) > 1:
        flips = content[1]
    else: flips = 1
    try: headsOdds = float(headsOdds)
    except: return await msg.channel.send("not a number")
    if headsOdds > 1 or headsOdds < 0:
        return await msg.channel.send("odds must be less than 1 and greater than 0")
    results = {}
    if int(flips) > 1:
        for _ in range(int(flips)):
            while True:
                f = random.random()
                if f != .5: break
            flip = "heads" if f <= headsOdds else "tails"
            try: results[flip] += 1
            except: results[flip] = 1
        embed = discord.Embed(title=f'Heads: {results["heads"]}\nTails: {results["tails"]}', color=0x00ff00)
    else:
        ans = "heads" if random.random() <= headsOdds else "tails"
        embed = discord.Embed(title=ans, color=0xff00ff if ans == "heads" else 0x0000ff)
    msg = await msg.channel.send(embed=embed)
    return await embedToReadableDict(msg, embed)

async def roleInfo(msg, content, cmd="roleinfo"):
    rolename = Content(content).strip()
    if not rolename:
        rolename = msg.author.top_role.name
    try:
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), msg.guild.roles)
        embed = discord.Embed(title=role.name, color=role.color)
        embed.add_field(name="id", value=role.id)
        embed.add_field(name="Color", value=f'RGB: {", ".join(tuple(str(x) for x in role.color.to_rgb()))}\nHEX: {role.color}')
        embed.add_field(name="displayed seperately?", value=role.hoist)
        embed.add_field(name="hierarchical position", value=len(msg.guild.roles) - role.position)
        embed.add_field(name="members with role", value=len(role.members))
        embed.add_field(name="Created at", value=await formatDateTime(role.created_at))
        msg = await msg.channel.send(embed=embed)
        return await embedToReadableDict(msg, embed)
    except AttributeError:
        return await msg.channel.send("role not found")

async def roleCount(msg, content, cmd="rolecount"):
    c = Content(content)
    Showroles = c @ "--showroles"
    c = c.string
    c = c.replace("!", "")[2:-1] if "<@" in c else c
    if not c: c = str(msg.author.id)
    m = findMember(c, msg)
    if m:
        roles = [x.mention for x in m.roles]
        roleCount = len(roles) - 1
        if Showroles:
            embed = discord.Embed(title=f"{m.name}'s Roles", color=m.color)
            embed.add_field(name="Count", value=roleCount)
            embed.add_field(name="Roles", value="".join(roles))
            msg = await msg.channel.send(embed=embed)
        else: msg = await msg.channel.send(roleCount)		
    else: msg = await msg.channel.send("User not found")
    return msg

async def rand(msg, content, cmd="rand"):
    global Stop
    if Stop: Stop = False
    content = Content(content)
    content.calcOps()
    Even = False if not content @ "--even" else True
    Odd = False if not content @ "--odd" else True
    content = content.split(" ")
    if len(content) > 1:
        r = int(content[2].strip()) if len(content) == 3 else 15
        low, high = int(content[0]), int(content[1])

        if not isInt(r): return await msg.channel.send("you are not rounding to a whole number")				
        if float(low) >= float(high): return await msg.channel.send("Low must be lower than high")

        if isInt(low) and isInt(high):
            while True:
                if Stop: await msg.channel.send(await stop("stopped picking a number"))
                res = random.randint(low, high)
                if Even and res % 2 != 0: continue					
                if Odd and res % 2 == 0: continue
                else: break
        else:
            res = random.uniform(float(low), float(high))
            if r: res = round(res, r)
    else: res = random.randint(1, 10)
    return await msg.channel.send(res)

async def compareRoles(msg, content, cmd="compareroles"):
    embed = discord.Embed(name="Role Comparison")
    c = Content(content).split(" ")
    user1 = str(c[0].strip()) 
    user2 = str(c[1].strip())
    if "<@" in user1:
        user1 = str(user1).replace("!", "")[2:-1]
    if "<@" in user2:
        user2 = str(user2).replace("!", "")[2:-1]
    u1name = findMember(user1, msg)
    u2name = findMember(user2, msg)
    if u1name and u2name:
        roles1 = {role.mention for role in u1name.roles}
        roles2 = {role.mention for role in u2name.roles}
        embed.add_field(name=f'{u1name} role count', value=len(roles1) - 1)
        embed.add_field(name=f'{u2name} role count', value=len(roles2) - 1)
        embed.add_field(name="both members", value="".join(roles1 & roles2), inline=False)
        embed.add_field(name=u1name, value="".join(roles1 - roles2), inline=False)
        embed.add_field(name=u2name, value="".join(roles2 - roles1), inline=False)
        await msg.channel.send(embed=embed)
    else: await msg.channel.send("invalid name(s)")

async def family(msg, content, cmd="family"):
    with open("family.txt", "r") as f: await oneLineCmd(msg, f.read())

async def mballreply(msg, content, cmd="mballreply"):
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    mssg = Content(content)
    if str(msg.author.id) in BOTMODS.keys():
        if cmd in BOTMODS[str(msg.author.id)]:
            with open(mballresponseFilePath, "a") as f:
                f.write(mssg + "\n")
            return await msg.channel.send("message added")				
    else: return await msg.channel.send("you don't have perms")

async def mballDel(msg, content, cmd="8brdel"):
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    reply = str(Content(content))
    if str(msg.author.id) in BOTMODS.keys():
        if cmd in BOTMODS[str(msg.author.id)]:
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
    try: await msg.delete()
    except: pass
    content = Content(content)
    content.calcOps()
    channel = discord.utils.get(msg.guild.channels, name="counting")
    highest = int(max([x.content.replace("*", "").replace("_", "").replace("`", "").strip(".") async for x in channel.history(limit=3)])) + 1
    async for x in channel.history(limit=1):
        if x.author == client.user: return ""
    text = f'.{highest}.'
    fancy = ""
    for op in content.ops_:
        if op == "--i":
            fancy += "*"
        if op == "--b":
            fancy += "**"
        if op == "--u":
            fancy += "__"
        if op == "--all":
            fancy += "***__"
    text = fancy + text + fancy[::-1]
    if "-e" in content:
        if "-c" in content:
            color = int(f'0x{content.split("-c")[1].strip()}', 16)
        else: color = 0x000000
        await channel.send(embed=discord.Embed(title=f'.{highest}.', color=discord.Color(color)))
    else: await channel.send(text)

async def choose(msg, content, cmd="choose"):
    content = Content(content)
    opOps = list(content.opsWithParams())
    embed = discord.Embed(title="picks")
    sep = " | "
    picks = 1
    for op, param in opOps:
        if op == "-picks": picks = int(param)
        if op == "-sep": 
            try: sep = {r'\n': "\n", r'\t': "\t"}[param]
            except: sep = param
    options = content.split("|", key=lambda x: x.strip())
    return await msg.channel.send(sep.join([random.choice(options) for _ in range(picks)]))

async def mball(msg, content, cmd="8ball"):
    with open(mballresponseFilePath, "rb") as f:
        await msg.channel.send(file=discord.File(f, "mballresponse.txt"))

async def pigLatin(msg, content, cmd="piglatin"):
    content = Content(content)
    if content.testOps("--kc"):
        content = content.lower()
    m = [x for x in content.split(" ") if x]
    for n, word in enumerate(m):
        if word[0] in "aeiou": m[n] += "ay"
        else:
            moveToEnd = [None if letter.lower() in "aeiou" else letter for letter in word] 
            moveToEnd = moveToEnd[:moveToEnd.index(None)] #all the letters until the first vowel represented by None
            m[n] = f'{word[len(moveToEnd):]}{"".join(moveToEnd)}ay'
    return await msg.channel.send(" ".join(m))

async def mostRoles(msg, content, cmd="mostroles"):
    content = Content(content).split(" ")[0]
    top = int(content) if content else 5
    memberRoles = {member.display_name.split("#")[0]: len(member.roles) - 1 for member in msg.guild.members}
    sortedKeys = sorted(memberRoles, key=memberRoles.get, reverse=True)
    top = [f'{r}, {memberRoles[r]}' for n, r in enumerate(sortedKeys) if n < top]
    return await msg.channel.send("\n".join(top))

async def clear(msg, content, cmd="clear"):
    content = Content(content)
    user = None
    length = None
    for op, param in content.opsWithParams({"user": (slice(0,None,None), " ")}):
        if op == "-user":
            user = content.getUser(msg, content=" ".join(param))
        if op == "-len":
            length = param
    amnt = int(content)
    if isBot(msg, client): return await msg.channel.send("nope")
    perms = msg.author.guild_permissions.manage_messages
    if perms and msg.author.id != 579117856994623498:
        if user and length: await msg.channel.purge(limit=amnt, check=lambda x: len(x.content) < int(length) and x.author == user)
        elif user: 
            await msg.channel.purge(limit=amnt, check=lambda x: x.author == user)
        elif length: 
            await msg.channel.purge(limit=amnt, check=lambda x: len(x.content) > int(length))
        else: await msg.channel.purge(limit=amnt)
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
        return await msg.channel.send("invites cleared")
    else: return await msg.channel.send("you don't have perms")

async def color(msg, content, cmd="color"):
    c = Content(content)
    user = c.getUser(msg, 0)
    if user != msg.author:
        color = user.color
        tempColor = str(color)[1:]
        r, g, b = int(tempColor[0:2], 16), int(tempColor[2:4], 16), int(tempColor[4:], 16)
        embed = discord.Embed(title=f'Hex: {str(color)}\nRGB: {r}, {g}, {b}', color=color)
        await msg.channel.send(embed=embed)
        return await embedToReadableDict(msg, embed)
        
    c = str(c)
    if "--rand" in c:
        ns = "0123456789abcdef"
        c = "#"
        for _ in range(6):
            c += random.choice(ns)

    if "#" in c:
        c = c.replace("#", "")
        r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:], 16)
        embed = discord.Embed(title=f'{r} {g} {b}', color=discord.Color(int(c, 16)))
        await msg.channel.send(embed=embed)
        return await embedToReadableDict(msg, embed)

    if ", " in c:
        c = c.replace(" ", "")
        color = [int(x) for x in c.split(",")]
        hexColor = [str(hex(x))[2:] for x in color]
        hexColor = list(map(lambda x: f'0{x}' if len(x) == 1 else x, hexColor))
        await msg.channel.send(embed=discord.Embed(title=f'#{"".join(hexColor)}', color=discord.Color.from_rgb(color[0], color[1], color[2])))	
        return await embedToReadableDict(msg, embed)

    if not c: c = str(msg.author.top_role)
    m = discord.utils.find(lambda r: r.name.lower() == c.lower(), msg.guild.roles)
    if m:
        embed = discord.Embed(title=str(m.color), color=m.color)
        await msg.channel.send(embed=embed)			
        msg.content = str(m.color)
        return msg		
    else: return await msg.channel.send("not a valid role")	

async def serverIcon(msg, content, cmd="servericon"):
    embed = discord.Embed(title="Server icon", color=discord.Colour.from_rgb(180, 70, 180))
    embed.set_image(url=msg.guild.icon_url)
    await msg.channel.send(embed=embed)
    return msg.guild.icon_url

async def channelInfo(msg, content, cmd="cc"):
    channel = msg.channel
    content = Content(content)
    if content:
        channel = discord.utils.find(lambda x: x.mention == str(content), msg.guild.channels)
    embed = discord.Embed(title=channel.name)
    created = channel.created_at
    diff = datetime.datetime.utcnow() - created
    pinCount = len(await channel.pins())
    if pinCount != 0: 
        if ":" in str(diff).split(" ")[0]:
            daysTillLastPin = (50-pinCount) / (pinCount / (int(str(diff).split(" ")[0].split(":")[0]) / 24))
        else: daysTillLastPin = (50-pinCount) / (pinCount / int(str(diff).split(" ")[0]))
    embed.add_field(name="Created at", value=await formatDateTime(created))
    embed.add_field(name="Pins", value=pinCount)
    if pinCount != 0: embed.add_field(name="days till last pin", value=str(daysTillLastPin))
    embed.add_field(name="time since creation", value=diff)
    embed.add_field(name="id", value=channel.id)
    embed.add_field(name="position", value=channel.position + 1)
    embed.add_field(name="slowmode delay", value=channel.slowmode_delay)
    embed.add_field(name="mention", value=channel.mention)
    embed.add_field(name="raw mention", value=f'\{channel.mention}')
    await msg.channel.send(embed=embed)

async def changes(msg, content, cmd="changes"):
    if "--raw" in content:
        with open("CHANGELOG.txt", "rb") as f: return await msg.channel.send(file=discord.File(f, "CHANGELOG.txt"))
    if "-date" in content:
        with open("CHANGELOG.txt", 'r') as f:
            date = content.split("-date ")[1]
            c = f.read().split("\n")
            vers = []
            lookFor = testInContent(content, "-my", "-m", "-day", "-y")
            if not lookFor:
                lookFor = "date"
            if lookFor:
                date = date.replace(f' {lookFor}', "")
            for line in c:
                ver = line.split(" ")[0]
                try:
                    m, d, y = line.split(" ")[-1].split("/")
                    m = m.strip("(")
                    y = y.strip(")")
                except: continue
                if lookFor == "-day" and d == date:
                    vers.append(ver)
                elif lookFor == "-m" and m == date:
                    vers.append(ver)
                elif lookFor == "-y" and y == date:
                    vers.append(ver)
                elif lookFor == "-my" and date.split("/")[0] == m and date.split("/")[1] == y:
                    vers.append(ver)
                elif date == f'{m}/{d}/{y}' and lookFor == "date":
                    vers.append(ver)
            return await msg.channel.send("\n".join(vers))
    ver = splitContent(content, " ")[1].strip() if testInContent(content, " ") else None
    if ver or not testInContent(content, "--nlatest"):
        with open("CHANGELOG.txt", "r") as f:
            if not ver:
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
        if testInContent(content, "--dms"): return await msg.author.send("\n".join(c)) if c else msg.author.send(file=discord.File(f, "changes.txt"))
        else: return await msg.channel.send("\n".join(c)) if c else await msg.channel.send(file=discord.File(f, "changes.txt")) 

async def hexBinOct(msg, content, cmd="hex"):
    content = str(Content(content))
    num = list(map(lambda n: int(n.strip()), content.split("|"))) if "|" in content else [int(content)]
    repWith = {"hex": "0x", "bin": "0b", "oct": "0o", "tobase": ""}[cmd]
    ans = list(map(lambda n: str(hex(n)).replace(repWith, ""), num))
    return await msg.channel.send(", ".join(ans))

async def response(msg, content, cmd="response"):
    global Stop
    if Stop: Stop = False
    if isBot(msg, client): return "is bot"
    limit = 1000
    content = Content(content)
    for op, param in content.opsWithParams():
        if "-lim" == op:
            limit = int(param)
            if limit > 100000:
                return await msg.channel.send("you cannot go above 100k")
            break
    mssg = str(content).strip()
    async with msg.channel.typing():
        hist = [m.content async for m in msg.channel.history(limit=limit)]
        responses = [hist[n - 1] for n, message in enumerate(hist) if message == mssg]
        if responses: msg = await msg.channel.send(f'{msg.author.mention} I HAVE FOUND A RESPONSE\n{random.choice(responses)}')
        else: msg = await msg.channel.send(f'did not find {mssg} in the past {limit} messages in this channel')
        return msg

async def stopwatch(msg, content, cmd="stopwatch"):
    content = Content(content)
    with open(timersPath, "r+") as tJ:
        data = json.load(tJ)
        running = data.get(str(msg.author.id))
        stopAt = content.toSet() & {"seconds", "minutes", "hours", "days", "weeks"}
        if not running:
            data[msg.author.id] = time.time()
            await msg.channel.send(f'{msg.author.mention} stopwatch started')
        elif running and content @ "--stop":
            t = await formatSeconds(time.time() - running)
            await msg.channel.send(embed=discord.Embed(title=str(round(t[0], 2)) + f' {t[1]}'))
            del data[str(msg.author.id)]
            return await msg.channel.send("timer stopped")
        elif stopAt:
            stopAt = list(stopAt)[0]
            t, layer = await formatSeconds(time.time() - running, stopAt=stopAt)
            r = 15 if not splitContent(content, f'{stopAt} ', index=1) else int(content.split(f'{stopAt} ')[1])
            t = round(t, r)
            await msg.channel.send(embed=discord.Embed(title=f'{t} {layer}'))
        elif running:
            t = await formatSeconds(time.time() - running)
            await msg.channel.send(embed=discord.Embed(title=str(round(t[0], 2)) + f' {t[1]}'))
        clearFile(tJ)
        json.dump(data, tJ)
        

async def emoteInfo(msg, content, cmd="emoteinfo"):
    emote = await msg.guild.fetch_emoji(int(content.split(":")[2][:-1]))
    embed = discord.Embed(title=emote.name)
    embed.set_thumbnail(url=emote.url)
    embed.add_field(name="Animated", value=emote.animated)
    embed.add_field(name="Added by", value=emote.user)
    embed.add_field(name="created at", value=await formatDateTime(emote.created_at))
    embed.add_field(name="id", value=emote.id)
    embed.add_field(name="Image", value=str(emote.url))
    embed.add_field(name="raw mention", value=f"\<:{emote.name}:707773683854213140>")
    await msg.channel.send(embed=embed)

async def messageInfo(msg, content, cmd="messageinfo"):
    sendTo = msg.channel
    content = Content(content)
    fetchFrom = msg.channel
    if msg.channel_mentions:
        fetchFrom = msg.channel_mentions[0]
        content = content.replace(fetchFrom.mention,  "", ret=True).strip()
    if content.isnumeric():
        try: msg = await fetchFrom.fetch_message(content)
        except discord.errors.NotFound:
            return await msg.channel.send("sorry that message wasn't found")
    if not msg.content:
        return await msg.channel.send("sorry that message doesn't exist")
    embed = discord.Embed(title="message info")
    embed.add_field(name="is tts", value=msg.tts)
    embed.add_field(name="author", value=msg.author.mention)
    embed.add_field(name="content", value=msg.content)
    embed.add_field(name="channel", value=msg.channel.mention)
    embed.add_field(name="id", value=msg.id)
    if msg.mentions:
        embed.add_field(name="member mentions", value=" ".join([x.mention for x in msg.mentions]))
    if msg.channel_mentions:
        embed.add_field(name="channel mentions", value=" ".join([x.mention for x in msg.channel_mentions]))
    if msg.role_mentions:
        embed.add_field(name="role mentions", value=" ".join([x.mention for x in msg.role_mentions]))
    embed.add_field(name="pinned", value=msg.pinned)
    embed.add_field(name="created at", value=await formatDateTime(msg.created_at))
    embed.add_field(name="jump to link", value=msg.jump_url)

    msg = await sendTo.send(embed=embed)
    return await embedToReadableDict(msg, embed)

async def typeFor(msg, content, cmd="type"):
    content = Content(content)
    timeToType = int(content) if content else 5
    if timeToType > 420:
        return await msg.channel.send("sorry thats too long")
    async with msg.channel.typing():
        await asyncio.sleep(timeToType)
    return await msg.channel.send(f'typed for {timeToType} seconds')

async def sendBlank(msg, content, cmd="sendblank"):
    content = Content(content)
    amnt = int(content) if content else 5
    msg = await msg.channel.send("_" + ("\n" * amnt) + "_")
    if msg.channel.name == "waddles_and_talkles":
        await msg.channel.send("https://media.discordapp.net/attachments/693893222006521856/730483647857033257/Screen_Shot_2020-07-08_at_2.00.35_PM.png")
    return msg

async def hangman(msg, content, cmd="hangman"):
    content = Content(content)
    user = content.getUser(msg, 0)
    if user.id in playingHangman.keys():
        return await msg.channel.send(f'{msg.author.mention} {user.name} is already in a game')
    try: lives = int(content.split(" ")[1])
    except: lives = 9
    playingHangman[user.id] = None
    await msg.author.send(f"you will have 15 seconds to send a word of your choice, and {user.name} will have to guess it in {msg.channel.name}")
    await asyncio.sleep(15)
    async for i in msg.author.dm_channel.history(limit=1):
        word = i.content
    disp = "".join(["-" if x not in [" ", "," "." "'" '"'] else x for x in word])
    playingHangman[user.id] = {"word": word, "lives": lives, "guessed": [], "disp": disp}
    await msg.channel.send(f'{user.mention} guessing time')
    mssg = await msg.channel.send(disp)
    try: await client.wait_for("message", check=lambda message: message.author.id == user.id, timeout=90.0)
    except: return await msg.channel.send("user did not respond in 1.5 minutes")
    else: return mssg

async def serverInfo(msg, content, cmd="serverinfo"):
    roles = msg.guild.roles
    creation = msg.guild.created_at
    t = datetime.datetime.now()
    embed = discord.Embed(title="Server Info", color=roles[-1].color)
    embed.set_thumbnail(url=msg.guild.icon_url)
    embed.add_field(name="icon link", value=msg.guild.icon_url)
    embed.add_field(name="icon animated?", value=msg.guild.is_icon_animated())
    embed.add_field(name="splash link", value=msg.guild.splash_url)
    embed.add_field(name="region", value=msg.guild.region)
    embed.add_field(name="emojis", value=f'{len(msg.guild.emojis)}/{msg.guild.emoji_limit * 2}')
    embed.add_field(name="filesize limit", value=msg.guild.filesize_limit)
    embed.add_field(name="guild id", value=msg.guild.id)
    embed.add_field(name="boost count", value=msg.guild.premium_subscription_count)
    embed.add_field(name="boosters", value="\n".join([x.mention for x in msg.guild.premium_subscribers]))
    embed.add_field(name="category count", value=len(msg.guild.categories))
    embed.add_field(name="channel count", value=len(msg.guild.channels))
    embed.add_field(name="voice channel count", value=len(msg.guild.voice_channels))
    embed.add_field(name="text channel count", value=len(msg.guild.text_channels))
    embed.add_field(name="roles", value=len(roles))
    embed.add_field(name="members", value=msg.guild.member_count)
    embed.add_field(name="owner", value=msg.guild.owner.mention)
    embed.add_field(name="creation time", value=await formatDateTime(creation))
    embed.add_field(name="age", value=t - creation)
    await msg.channel.send(embed=embed)

async def userInfo(msg, content, cmd="userinfo"):
    user = (await getUserInContent(msg, content, cmd))
    embed = discord.Embed(title=user.name, color=user.color)
    embed.add_field(name="Join date", value=await formatDateTime(user.joined_at))
    embed.add_field(name="nick name", value=user.nick)
    embed.add_field(name="color", value=f'RGB: {", ".join(tuple(str(x) for x in user.color.to_rgb()))}\nhex: {user.color}')
    embed.add_field(name="role count", value=len(user.roles))
    embed.add_field(name="avatar url", value=user.avatar_url)
    embed.add_field(name="created at", value=await formatDateTime(user.created_at))
    embed.add_field(name="discriminator", value=user.discriminator)
    embed.add_field(name="id", value=user.id)
    embed.add_field(name="mention", value=user.mention)
    embed.add_field(name="raw mention", value=f'\{user.mention}')
    embed.add_field(name="roles", value=" ".join([x.mention for x in user.roles]), inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    await msg.channel.send(embed=embed)

async def fetchRole(msg, content, cmd="fetchrole"):
    role = msg.guild.get_role(int(Content(content)))
    return await msg.channel.send(role.name)

async def categoryInfo(msg, content, cmd="categoryinfo"):
    content = Content(content).string
    cat = discord.utils.find(lambda x: x.name.lower() == content.lower(), msg.guild.categories)
    embed = discord.Embed(title=cat.name)
    embed.add_field(name="id", value=cat.id)
    embed.add_field(name="position", value=cat.position)
    embed.add_field(name="channels", value=len(cat.channels))
    embed.add_field(name="text channels", value=len(cat.text_channels))
    embed.add_field(name="voice channels", value=len(cat.voice_channels))
    embed.add_field(name="created at", value=await formatDateTime(cat.created_at))
    msg = await msg.channel.send(embed=embed)
    return await embedToReadableDict(msg, embed)

async def spamStop(msg, content, cmd="spamstop"):
    for _ in range(10):
        await msg.channel.send(f'{PREFIX}stop')
        await asyncio.sleep(random.uniform(.3, 1.2))

async def calc(msg, content, cmd="calc"):
    content = Content(content)
    if not content.suitibleForEval():
        return await msg.channel.send('nice try')
    else: 
        try:
            return await msg.channel.send(eval(str(content)))
        except Exception as e:
            print(e)
            return await msg.channel.send(str(type(e)).split(' ')[1].split("'")[1].strip("'"))

async def pokemon(msg, content, cmd="pokemon"):
    pokemon = Content(content)
    try:
        request = requests.get(f"https://www.pokemon.com/us/pokedex/{pokemon}")
        soup = bs.BeautifulSoup(request.text, features="html.parser")
        name_id = soup.find("div", {"class": "pokedex-pokemon-pagination-title"})
        name = name_id.find("div").text
        embed = discord.Embed(title=name.replace("\n", ""))
        img = soup.find("img", {"class": "active"})["src"]
        div = soup.find("div", {"class": "pokemon-ability-info color-bg color-lightblue match active"})
        titles = div.find_all("span", {"class": "attribute-title"})
        values = div.find_all("span", {"class": "attribute-value"})
        attrs = {name.text: value.text for name, value in zip(titles, values)}
        for key, item in attrs.items():
            if key == "Gender": continue
            embed.add_field(name=key, value=item)
        embed.set_thumbnail(url=img)
        embed.set_footer(text=f'source: https://www.pokemon.com/us/pokedex/{pokemon}')
        msg = await msg.channel.send(embed=embed)
        return await embedToReadableDict(msg, embed)
    except Exception as e: 
        print(e)
        return await msg.channel.send("smth went wrong")

async def hypixelPlayerCount(msg, content, cmd="hypixelpc"):
    game = Content(content).string
    if game:
        data = requests.get(f"https://api.hypixel.net/gameCounts?key={HPKEY}").json()
        if game == "list":
            return await msg.channel.send(", ".join(list(x.lower() for x in data["games"].keys())))
        gameData = data["games"].get(game.upper())
        if gameData:
            embed = discord.Embed(title=game, color=discord.Color(0xffff00))
            embed.add_field(name=game, value=gameData["players"])
            modes = gameData.get("modes")
            if modes:
                for mode in modes.items():
                    embed.add_field(name=mode[0], value=mode[1])
            return await msg.channel.send(embed=embed)
    return await msg.channel.send(requests.get(f"https://api.hypixel.net/playercount?key={HPKEY}").json()["playerCount"])

async def hypixelBanStats(msg, content, cmd="hypixelban"):
    data = requests.get(f"https://api.hypixel.net/watchdogstats?key={HPKEY}").json()
    embed = discord.Embed(title="ban stats", color=discord.Color(0xffff00))
    for k, v, in data.items():
        if k == "success": continue
        else: embed.add_field(name=k, value=v)
    return await msg.channel.send(embed=embed)

async def whoHasRole(msg, content, cmd="hasrole"):
    role = Content(content)
    role.calcOps()
    Raw = False if not role @ "--file" else True
    role = discord.utils.find(lambda r: r.name.lower() == role.lower().strip(), msg.channel.guild.roles)
    if not role: return await msg.channel.send("role not found")
    has = [user.mention for user in msg.channel.guild.members if role in user.roles]
    try: 
        if Raw: raise FileException("wanted file")
        embed = discord.Embed(title=role.name, color=role.color)   
        embed.add_field(name="has", value="\n".join(has))
        await msg.channel.send(embed=embed)
        msg.content = "\n".join([user.name for user in msg.channel.guild.members if role in user.roles])
        return msg
    except Exception as e:
        if not has:
            return await msg.channel.send(f'no one has {role.name}')
        if type(e) != FileException:
            await msg.channel.send("too many chars, here's a text file")
        has = [f'NAME: {user.name}\nID: {user.id}' for user in msg.channel.guild.members if role in user.roles]
        with open(f"whohas{role.name}.txt", "w") as f:
            f.write("\n\n".join(has))
        with open(f'whohas{role.name}.txt', "rb") as f:
            await msg.channel.send(file=discord.File(f, f'whohas{role.name}.txt'))
        os.remove(f"whohas{role.name}.txt")

async def addCustomCmd(msg, content, cmd="customcmd"):
    global CATS, CMDLIST, CUSTOMCMDS
    content = Content(content)
    Locked = False if not content @ "--lock" else True
    c = content.split("|")
    name = c.pop(0).strip()
    say = c.pop(0)
    if " " in name: return await msg.channel.send("no spaces in command names")
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for cmd in data:
            if cmd["name"] == name:
                return await msg.channel.send("already a command")
        params = ""
        if "{content}" in say:
            params += " <message>"
        if datetime.datetime.now().strftime("%Y") == "2020":
            d = datetime.datetime.now().strftime("%m/%d/%Y")
        else:
            d = datetime.datetime.now().strftime("%m/%d/%y")
        data.append({"name": name, "desc": say, "params": params, "date": d, "Locked": Locked, "addedby": str(msg.author.id), "editedby": []})
        mssg = await msg.channel.send("added")
        clearFile(j)
        json.dump(data, j)
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    return mssg

async def removeCustomCmd(msg, content, cmd="removecustomcmd"):
    global CATS, CMDLIST, CUSTOMCMDS
    perms = msg.author.guild_permissions.manage_messages
    if not perms and str(msg.author.id) not in BOTMODS.keys():
        return await msg.channel.send("you cannot do that")
    name = content[len(cmd) + 2:].split()
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for cmd in data:
            if cmd["name"] in name:
                if cmd.get("Locked"):
                    try:
                        await msg.channel.send(f"{msg.author.mention} this command is locked are you sure") 
                        YN = await client.wait_for("message", check=lambda message: message.author.id == msg.author.id, timeout=60.0)
                    except:
                        return await msg.channel.send("cancelled")
                    if YN.content.lower() in ["no", "cancel", 'stop', 'n']:
                        return await msg.channel.send("cancelled")
                data.remove(cmd)
                name.remove(cmd["name"])
        if name: return await msg.channel.send(f"{', '.join(name)} not found")
        clearFile(j)
        json.dump(data, j)
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    return await msg.channel.send(f'removed {" ".join(name)}')

async def deathBattle(msg, users, going, notGoing, responseTime, damageMsgs, healMsgs, embed, first, second, editable):
    global playingDB, Stop
    if Stop: 
        Stop = False
        await removeFromList(playingDB, going, notGoing) 
    tempItems = {item["id"]: item["name"].lower() for item in users[going]["items"]} #gets the items + item ids ready
    temp = await msg.channel.send(f"{going.name} attack or heal\nor item (there is no backing out)") #message to say in chat
    try: #waiting for option
        ah = await client.wait_for("message", check=lambda message: message.author.id == going.id and message.content.lower() in ["attack", "a", "h", "heal", "stop", "item"], timeout=responseTime)
        AH = ah.content.lower()
        await ah.delete()
    except: #didnt' pick in time
        AH = random.choice(["attack", "heal"])
        await msg.channel.send(f"you waited too long you I picked {AH} for you")
    CustomMessage = False
    if AH == "item":
        newLine = "\n"
        if not users[going]["items"]:
            await msg.channel.send("you don't have items")
            AH = "attack"
        else: 
            whichItem = await msg.channel.send(f"which item (say a number)\n{newLine.join([f'{idd}: {name}' for idd, name in tempItems.items()])}") #says list of items user has
            try:
                i = await client.wait_for("message", check=lambda message: message.author.id == going.id and message.content.lower().isnumeric()) #waits for pick
                await i.delete()
                i = int(i.content.lower())
            except: #waited too long
                await msg.channel.send("you waited to long, picking 1")
                i = 1
            await whichItem.delete()
            with open(itemDataFilePath, "r+", encoding="utf-8-sig") as j: #removes from inventory
                data = json.load(j)
                for item in data[str(going.id)]:
                    if item["id"] == i:
                        AH = item["name"]
                        data[str(going.id)].remove(item)
                users[going]["items"] = data[str(going.id)]
                clearFile(j)
                json.dump(data, j)
            CustomMessage = True
            if AH.title() == "Theft":
                count = 0
                while AH.title() == "Theft":
                    if not users[notGoing]["items"]:
                        await msg.channel.send("your opponent doesn't have any items\ndealing 20 damage")
                        users[notGoing]["health"] -= 20
                        CustomMessage = f'{going} did 20 damage to {notGoing}'
                        break
                    else:
                        AH = random.choice(users[notGoing]["items"])["name"]
                        if AH.title() == "Theft":
                            temp = notGoing
                            notGoing = going
                            going = temp
                    count += 1
                    if count > 1000: 
                        await msg.channel.send("1000 limit reached, nothing happens")
                        CustomMessage = 'nothing happened'
                        temp = notGoing
                        notGoing = going
                        going = temp
                        break
            if AH.title() == "Epic Match":
                try:
                    await msg.channel.send("what health should each player be set to you have 60 seconds") 
                    health = await client.wait_for("message", check=lambda message: message.author == going and message.content.isnumeric(), timeout=60.0)
                except:
                    await msg.channel.send("you waited too long, picking 15")
                health = float(health.content)
                if health > 200:
                    await msg.channel.send("too high, you get to do NOTHING")
                    if going == first:
                        await deathBattle(msg, users, second, first, responseTime, damageMsgs, healMsgs, embed, first, second, editable)
                    else: await deathBattle(msg, users, first, second, responseTime, damageMsgs, healMsgs, embed, first, second, editable)
                else:
                    users[going]["health"] = health
                    users[notGoing]["health"] = health
                    CustomMessage = f'both players have been set to {health} hp'
            if AH.title() == "Even Match":
                users[going]["health"] = 100
                users[notGoing]["health"] = 100
                CustomMessage = f'both players have been set to 100 hp'
            if AH.title() == "Swap":
                t1 = users[going]["health"]
                t2 = users[notGoing]["health"]
                users[going]["health"] = t2
                users[notGoing]["health"] = t1
            if AH.lower() == "life or death":
                die = random.choice([going, notGoing])
                users[die]["health"] -= (users[die]["health"] + random.randint(0, 70))
                CustomMessage = f'{die} has just died\nRIP'
            if AH.lower() == "healing":
                users[going]["health"] += 40
                damage = -40
                CustomMessage = f'{going} used healing for 40 health'
            if AH.upper() == "RANDOM HEAL!!":
                add = random.randint(0, 100)
                users[going]["health"] += add
                damage = -add
                CustomMessage = f'{going} RANOMLY HEALED and got {add} more health!!!!11!1!1'
            if AH.lower() == "duel-edged sword":
                users[notGoing]["health"] -= 40
                users[going]["health"] -= 15
                damage = 40
                CustomMessage = f'{notGoing} took 40 damage and {going} took 15 damage in the process'
    if AH in ["attack", "a"]:
        damage = round(random.gauss(25, 5), 0)
        await temp.delete()
    elif AH in ["h", "heal"]: 
        if users[going]["health"] >= 100:
            await msg.channel.send("you can't go above the limit\npicking damage")
            damage = round(random.gauss(25, 5), 0)
        else:
            damage = round(random.gauss(-24, 5), 0)
            await temp.delete()
    elif AH == 'stop':
        await addMoney(going, -20)
        await removeFromList(playingDB, going, notGoing) 
        await temp.delete()
        return await stop("stopped")
    if not CustomMessage:
        if damage < 0:
            users[going]["health"] -= damage
        else:
            users[notGoing]["health"] -= damage
    if CustomMessage: move = CustomMessage
    elif damage > 0: move = random.choice(damageMsgs).replace("{attaker}", going.mention).replace("{aked}", notGoing.mention).replace("{damage}", str(damage))
    else: move = random.choice(healMsgs).replace("{attaker}", going.mention).replace("{aked}", notGoing.mention).replace("{damage}", str(abs(damage)))

    ED = embed.to_dict()
    for d in ED["fields"]:
        if d["name"] == "MOVE":
            d["value"] = move
        elif d["name"] == first.name:
            d["value"] = str(users[first]["health"])
        elif d["name"] == second.name:
            d["value"] = str(users[second]["health"])
    embed = embed.from_dict(ED)
    async for msssg in editable.channel.history(limit=5):
        if msssg.author == editable.author and msssg.embeds: 
            await editable.edit(embed=embed)
            break
    else:
        editable = await msg.channel.send(embed=embed)
    if users[second]["health"] <= 0 and users[first]["health"] <= 0:
        await removeFromList(playingDB, going, notGoing)
        return await msg.channel.send("ITS A DRAW!")
    if users[second]["health"] <= 0:
        await removeFromList(playingDB, going, notGoing) 
        await addMoney(first, abs(users[second]["health"]))
        await addMoney(second, users[second]["health"])
        return await msg.channel.send(f'{first.name} has won!\nthey earned {abs(users[second]["health"])} and {second.name} has lost {abs(users[second]["health"])}')
    elif users[first]["health"] <= 0:
        await removeFromList(playingDB, going, notGoing) 
        await addMoney(second, abs(users[first]["health"]))
        await addMoney(first, users[first]["health"])
        return await msg.channel.send(f'{second.name} has won!\nthey earned {abs(users[first]["health"])} and {first.name} has lost {abs(users[first]["health"])}')
    else:
        if going == first:
            await deathBattle(msg, users, second, first, responseTime, damageMsgs, healMsgs, embed, first, second, editable)
        else: await deathBattle(msg, users, first, second, responseTime, damageMsgs, healMsgs, embed, first, second, editable)

async def INIT_deathBattle(msg, content, cmd="deathbatte"):
    global Stop, playingDB
    if Stop: Stop = False
    embed = discord.Embed(title="BATTLE")
    responseTime = random.uniform(8, 10)
    if testInContent(content, " -t"):
        responseTime = float(splitContent(content, "-t ", index=1))
        content = splitContent(content, " -t")[0]
    user2 = await getUserInContent(msg, content, cmd)
    if msg.author in playingDB:
        return await msg.channel.send(f'{msg.author.name} is in a game')
    if user2 in playingDB:
        return await msg.channel.send(f'{user2.name} is in a game')
    if msg.author == client.user or user2 == client.user:
        return await msg.channel.send("I cannot play sadly :((((((")
    with open(levelingDataFilePath, "r") as j:
        data = json.load(j)
        b1 = data[str(msg.author.id)]["level"] // 3
        if data.get(str(user2.id)):
            b2 = data[str(user2.id)]["level"] // 3
        else: b2 = 0
    first = random.choice([msg.author, user2])
    second = msg.author if first == user2 else user2
    playingDB.append(first)
    playingDB.append(second)
    with open(itemDataFilePath, "r", encoding="utf-8-sig") as j:
        data = json.load(j)
        items = data.get(str(msg.author.id))
        if items:
            i1 = items
        else: i1 = []
        items = data.get(str(user2.id))
        if items:
            i2 = items
        else: i2 = []
    users = {msg.author: {"user": msg.author, "health": 100 + b1, "items": i1},
             user2: {"user": user2, "health": 100 + b2, "items": i2}}
    users[second]["health"] += 15
    embed.add_field(name="MOVE", value="START", inline=False)
    for user in users.values():
        embed.add_field(name=user["user"].name, value=user["health"])
    damageMsgs = ["{attaker} punched {aked} for {damage}", "{attaker} fireballed {aked} for {damage}", "{attaker} summoned a meteor and it hit {aked} for {damage}", "{aked} was unconsious and a pickle came FLYING at {aked} they took {damage} damage"]
    healMsgs = ["{attaker} was healed for {damage}", "{attaker} was blessed with {damage} extra health"]
    editable = await msg.channel.send(embed=embed)    
    await deathBattle(msg, users, first, second, responseTime, damageMsgs, healMsgs, embed, first, second, editable)
    
async def mmoney(msg, content, cmd="mmoney"):
    user = Content(content).getUser(msg, 0)
    if testInContent(content, "--raw"):
        with open(moneyDataFilePath, "rb") as f:
            await msg.channel.send(file=discord.File(f, "money.json"))
    with open(moneyDataFilePath, "r") as j:
        data = json.load(j)
        return await msg.channel.send(f'{user.name} has €{data.get(str(user.id))}')

async def shop(msg, content, cmd="shop"):
    with open(itemsFilePath, "r") as j:
        data = json.load(j)
        embed = discord.Embed(title="Items", color=discord.Color(0x00ff00))
        for item in data:
            embed.add_field(name=f'{item["id"]}: {item["name"]}', value=f'Description: {item["desc"]}\nCost: €{item["cost"]}')
        await msg.channel.send(embed=embed)

async def buyItem(msg, content, cmd="buyitem"):
    buying = Content(content).string
    if ", " in content:
        amnt = int(content.split(", ")[1])
        buying = content.split(", ")[0]
    else: amnt = 1
    with open(moneyDataFilePath, "r") as j:
        data = json.load(j)
        money = data.get(str(msg.author.id))
        if not money: return await msg.channel.send("you have no money")
    with open(itemsFilePath, "r") as j:
        data = json.load(j)
        for item in data:
            if item["name"].lower() == buying.lower() or item["id"] == int(buying):
                forPurchase = item; break
        else: return await msg.channel.send("did not find item")
    amountBought = 0
    for _ in range(amnt):
        if money < forPurchase["cost"]: return await msg.channel.send("you don't have enough money")
        else:
            money -= forPurchase["cost"]
            amountBought += 1
    with open(itemDataFilePath, "r+", encoding="utf-8-sig") as j2:
        data = json.load(j2)
        l = data.get(str(msg.author.id))
        if l: 
            for _ in range(amountBought):
                l.append(forPurchase)
        else: l = [forPurchase] * amountBought
        data[str(msg.author.id)] = l
        clearFile(j2)
        json.dump(data, j2)
    with open(moneyDataFilePath, "r+") as j:
        data = json.load(j)
        data[str(msg.author.id)] = money
        clearFile(j)
        json.dump(data, j)
    await msg.channel.send(f'bought {forPurchase["name"]}')

async def inventory(msg, content, cmd="inv"):
    with open(itemDataFilePath, "r+", encoding="utf-8-sig") as j:
        data = json.load(j)
        items = data.get(str(msg.author.id))
        if items:
            embed = discord.Embed(name=f"{msg.author.name}'s inventory", color=msg.author.color)
            s = {item["name"] for item in items}
            count = {item: 0 for item in s}
            used = []
            for item in items: count[item["name"]] += 1
            for item in items:
                if item in used:
                    continue
                used.append(item)
                embed.add_field(name=f'{item["name"]} * {count[item["name"]]}', value=f'{item["name"]}: {item["desc"]}',)
            await msg.channel.send(embed=embed)
            del used
            del count
            del s
        else: return await msg.channel.send("none")

async def duplicator(msg, content, cmd="duplicator"):
    t = Content(content)
    times = 2
    if t.split(" ")[0].isnumeric():
        times = int(t.split(" ")[0])
        t = t.replace(f'{times}', "", ret=True).strip()
    try: return await msg.channel.send(f'{t} '*times)
    except: return await msg.channel.send("message too long, try reducing the number of duplications")

async def customCmdList(msg, content, cmd="customcmdlist"):
    _, _, CUSTOMCMDS = await reloadCMDSLIST()
    content = Content(content)
    if content @ "--raw":
        with open(customcmdsFilePath, "rb") as f: await msg.channel.send(file=discord.File(f, "customCmds.json"))
    else: 
        try:
            if content @ "--file": raise FileException("wanted file")
            content = await oneLineCmd(msg, "\n".join([f'{x}: {y}' for x, y in CUSTOMCMDS.items()]))
        except:
            write = ""
            with open(customcmdsFilePath, "r") as j:
                data = json.load(j)
                for cmmd in data:
                    params = cmmd["params"]
                    desc = cmmd["desc"]
                    aliases = cmmd.get("aliases")
                    date = cmmd.get("date")
                    Locked = cmmd.get("Locked")
                    addedBy = cmmd.get("addedby")
                    editedBy = cmmd.get("editedby")
                    if aliases: aliases = ",\n".join(f'``{x}``' for x in aliases)
                    write += f'Name {cmmd["name"]}\n\nParams: {params}\n\nDescription: {desc}\n\nAliases: {aliases}\n\nDate added: {date}\n\nLocked: {Locked}\n\nAdded by: {addedBy}\n\nEdited by: {editedBy}\n\n\n\n'
            with open("customcmdlist.txt", "w") as f:
                f.write(write)
            with open("customcmdlist.txt", "rb") as f:
                await msg.channel.send(file=discord.File(f, "customcmdlist.txt"))
            os.remove("customcmdlist.txt")
async def editCustomCmd(msg, content, cmd="eccmd"):
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    content = Content(content)
    lookFor = content.split("|")[0].strip()
    changeTo = content.split("|", pastIndex=1)
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for command in data:
            if command["name"] == lookFor:
                if not command.get("Locked") or str(msg.author.id) in BOTMODS.keys() or str(msg.author.id) == command.get("addedby"):
                    if cmd not in BOTMODS[str(msg.author.id)]: return await msg.channel.send("cannot change that command it's locked")
                    if "--lock" in changeTo:
                        if not command.get("Locked"):
                            command["Locked"] = True
                        else:
                            command["Locked"] = command["Locked"]^True
                    else:
                        command["desc"] = changeTo
                    if command.get("editedby"): 
                        if str(msg.author.id) not in command["editedby"]:
                            command["editedby"] += [str(msg.author.id)]
                    else: command["editedby"] = [str(msg.author.id)]
                else: return await msg.channel.send("cannot change that command it's locked")
                break
        else: return await msg.channel.send("command doesn't exist")
        clearFile(j)
        json.dump(data, j)
    return await msg.channel.send("changed successfully")

async def luckynumber(msg, content, cmd="luckynumber"):
    content = Content(content)
    who = msg.author.mention
    count = 3
    for op, param in content.opsWithParams():
        if op == "-c":
            try: count = int(param)
            except: return await msg.channel.send("amount of numbers must be an integer")
    if content: who = content
    nums = " ".join([str(random.randint(1, 10)) for _ in range(count)])
    if random.random() >= .999: return await msg.channel.send(f"{who}'s lucky numbers are 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7")
    return await msg.channel.send(f"{who}'s lucky numbers are {nums}")

async def uptime(msg, content, cmd="uptime"):
    content = Content(content)
    stopAt = content.toSet() & {"seconds", "minutes", "hours", "days", "weeks"}
    if stopAt:
        stopAt = tuple(stopAt)[0]
        t, layer = await formatSeconds(time.time() - UPTIME, stopAt=stopAt)
        r = 15 if not splitContent(str(content), stopAt + " ") else int(splitContent(str(content), f'{stopAt} ')[1])
        await msg.channel.send(f'{round(t, r)} {layer}')
    else:
        if random.random() > .99: return await msg.channel.send("tbh i forget how long i've been on for sorry, i might remember later though")
        t, layer = await formatSeconds(time.time() - UPTIME) 
        return await msg.channel.send(f'{str(t)} {layer}')

async def editCmd(msg, content, cmd="edit"):
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-t" or op == "-time":
            if param == "instant":
                sleepFor = 0
            else:
                sleepFor = float(param)
                if sleepFor < 0:
                    return await msg.channel.send("must be greater than 0")
            break
    else: sleepFor = .7
    edits = content.split("|")
    editable = await msg.channel.send(edits[0])
    while edits:
        edits.pop(0)
        if not edits: break
        await asyncio.sleep(sleepFor)

        tokens = {"+": "add", 
        "-": False, 
        "*": "multiply",
        "<": "insertBeggining",
        "%": "replace",
        "^": "insert",
        ";": "newmessage"}
        token = tokens.get(edits[0][0])
        if token == None or token == "add": await editable.edit(content=editable.content + edits[0])
        elif token == "multiply": await editable.edit(content=editable.content*int(edits[0][1:]))
        elif token == "replace":
            rep = edits[0].split("%")[1].split(">>")[0]
            repWith = edits[0].split(">>")[1]
            await editable.edit(content=editable.content.replace(rep if rep != "MSG" else editable.content, repWith))
        elif token == "insert":
            pos = edits[0].split("^")[1].split(">>")[0]
            repWith = edits[0].split(">>")[1]
            l = [x for x in editable.content]
            l.insert(int(pos), repWith)
            await editable.edit(content="".join(l))
        elif token == "insertBeggining" and edits[0][1] == "<": 
            await editable.edit(content=f'{edits[0][2:]}' + editable.content)
        elif token == "newmessage":
            send = Content(edits[0].split(";")[1], removeCmd=False)
            if send @ "--delete":
                await editable.delete()
            editable = await editable.channel.send(send)

        else: await editable.edit(content=editable.content.replace(edits[0][1:], ""))
    return editable

async def pingResponse(msg, content, cmd="pingresponse"):
    response = Content(content)
    if isBot(msg, client): return
    with open(pingResponseFilePath, "r+") as j:
        data = json.load(j)
        if "-WHEN" in response:
            when = response.split("-WHEN ")[1]
            when = when.split(" ")
            data[str(msg.author.id)]["when"] = when
        elif response.lower() == "none":
            del data[str(msg.author.id)]
        else:
            if not data.get(str(msg.author.id)):
                data[str(msg.author.id)] = {"response": str(response), "when": ["offline"]}
            else:
                data[str(msg.author.id)] = {"response": str(response), "when": data[str(msg.author.id)]["when"]}
        clearFile(j)
        json.dump(data, j)
    if "-WHEN" in response:
        return await msg.channel.send(f'response will happen when you are {" ".join(data[str(msg.author.id)]["when"])}')
    return await msg.channel.send(f"changed to:\n{response}")

async def setStatus(msg, content, cmd="status"):
    st = Content(content)
    if len(st) > 1:
        await client.change_presence(activity=discord.Game(name=str(st)))
        return await msg.channel.send(f"changed to {st}")
    else: return await msg.channel.send("you didn't set the status to anything")

async def imageInfo(msg, content, cmd="imginfo"):
    att, *_ = await getImg(msg)
    
    embed = discord.Embed(title=att.filename if att.filename else "UNKNOWN.img")
    embed.add_field(name="id", value=att.id if att.id else "UNKOWN")
    embed.add_field(name="file size", value=att.size if att.size else "UNKOWN")
    embed.add_field(name="width", value=att.width if att.width else "UNKOWN")
    embed.add_field(name="height", value=att.height if att.height else "UNKOWN")
    embed.add_field(name="url", value=att.url if att.url else "UNKOWN")
    embed.add_field(name="spoiler?", value=att.is_spoiler if type(att.is_spoiler) is bool else "UNKNOWN")
    mssg = await msg.channel.send(embed=embed)
    return await embedToReadableDict(mssg, embed)

async def fileInfo(msg, content, cmd="fileinfo"):
    att, filename, url = await getImg(msg)

    await saveImg(filename, url)
    with open(filename, "r") as f:
        read = f.read()
    charCount = len(read)
    wordCount = len(read.split(" "))
    charCountEXWhiteSpace = len(re.sub("\s+", "", read))
    letterCount = len(re.findall("[A-Za-z]", read))
    numberCount = len(re.findall("[0-9]", read))

    embed = discord.Embed(title=att.filename if att.filename else "UNKNOWN")
    embed.add_field(name="id", value=att.id if att.id else "UNKNOWN")
    embed.add_field(name="file size", value=att.size if att.size else "UNKNOWN")
    embed.add_field(name="word count", value=wordCount)
    embed.add_field(name="character count", value=charCount)
    embed.add_field(name="char count ex spaces/whitespace", value=charCountEXWhiteSpace)
    embed.add_field(name="letter count", value=letterCount)
    embed.add_field(name="number count", value=numberCount)
    mssg = await msg.channel.send(embed=embed)
    os.remove(filename)
    return await embedToReadableDict(msg, embed)

async def textInfo(msg, content, cmd="textinfo"):
    text = Content(content)
    Re = False
    sep = " "
    for op, param in text.opsWithParams():
        if op in ("-re", "-regex"):
            Re = True
    try:
        att, filename, url = await getImg(msg, NotFromChat=True)
        await saveImg(filename, url)
        with open(filename, "r") as f:
            text = Content(f.read(), removeCmd=False)
    except:
        pass
    if Re:
        find = re.findall(str(param), str(text))
        try: return await msg.channel.send(sep.join(find))        
        except Exception as e:
            print(e)
            if type(e) is discord.errors.HTTPException:
                if not find:
                    return await msg.channel.send("did not find any match")
                else:
                    with open("match.txt", "w") as f:
                        f.write(sep.join(find))
                    with open("match.txt", "rb") as f:
                        return await msg.channel.send("message too long", file=discord.File(f, "match.txt"))
    RankWords = False if not text @ "--rankwords" else True
    text = str(text)
    if not RankWords:
        charCount = len(text)
        wordCount = len(text.split(" "))
        charCountEXWhiteSpace = len(re.sub(r"\s+", "", text))
        letterCount = len(re.findall(r"[A-Za-z]", text))
        capitalLetters = len(re.findall(r"[A-Z]", text))
        lowerLetters = len(re.findall(r"[a-z]", text))
        numberCount = len(re.findall(r"[0-9]", text))
        whiteSpaceCount = len(re.findall(r'\s', text))
        averageWordLength = statistics.mean([len(word) for word in text.split()])

    words = {}
    for word in text.split():
        try:
            words[word] += 1
        except:
            words[word] = 1

    sortedWords = sorted(words.items(), key=lambda x: x[1], reverse=True)
    if not RankWords:
        embed = discord.Embed(title="Text info")
        embed.add_field(name="most common word", value=f'{sortedWords[0][0]}: {sortedWords[0][1]}')
        embed.add_field(name="word count", value=wordCount)
        embed.add_field(name="average word length", value=averageWordLength)
        embed.add_field(name="character count", value=charCount)
        embed.add_field(name="char count ex spaces/whitespace", value=charCountEXWhiteSpace)
        embed.add_field(name="white space count", value=whiteSpaceCount)
        embed.add_field(name="letter count", value=letterCount)
        embed.add_field(name="capital letters", value=capitalLetters)
        embed.add_field(name="lowercase letters", value=lowerLetters)
        embed.add_field(name="number count", value=numberCount)
    else:
        send = ""
        for word in sortedWords:
            send += f'{word[0]}: {word[1]}\n'
        try:
            return await msg.channel.send(send)
        except:
            with open(f'{msg.author.id}.txt', "w") as f:
                f.write(send)
            with open(f'{msg.author.id}.txt', "rb") as f:
                return await msg.channel.send(file=discord.File(f, "text.txt"))
            os.remove(f'{msg.author.id}.txt')
    return await msg.channel.send(embed=embed)

async def embedInfo(msg, content, cmd="embedtotext"):
    sendTo = msg
    content = Content(content).string
    fetchFrom = msg.channel
    if msg.channel_mentions:
        fetchFrom = msg.channel_mentions[0]
        content = content.replace(fetchFrom.mention,  "").strip()
    if content.isnumeric():
        try: embed = (await fetchFrom.fetch_message(content)).embeds[0]
        except discord.errors.NotFound:
            return await msg.channel.send("sorry that message wasn't found")
    if not msg.embeds:
        async for mssg in fetchFrom.history(limit=100):
            if mssg.embeds:
                embed = mssg.embeds[0]
                break
        else:
            async for mssg in msg.channel.history(limit=100):
                if mssg.embeds:
                    embed = mssg.embeds[0]
                    break
            return await msg.channel.send('no messages with embeds found')
    return await msg.channel.send((await embedToReadableDict(msg, embed)).content)

async def rotateImg(msg, content, cmd="rotateImg"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    Fit = True if not content @ "--nofit" else False
    if "https://" in content:
        content.replace(url, '')
    if len(content.split(" ")) == 1 and any(content.split(" ")):
        angle = int(content.split(" ")[0])
    else: angle = 90
            
    if not url: return await msg.channel.send("no img provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.rotate(int(angle), expand=Fit)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def mirrorImg(msg, content, cmd="mirrorimg"):
    content = Content(content)
    XY = content.split(" ")[0].lower()
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    if XY == "x":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif XY == "y":
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def spreadPixels(msg, content, cmd="spreadpixels"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    if content.split(" ")[0]:
        dist = int(content.split(" ")[0])
    else: dist = 100
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.effect_spread(dist)
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def filterImg(msg, content, cmd="filterimg"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    if content.split(" ")[0]:
        filt = content.split(" ")[0:]
    else: return await msg.channel.send("no filter provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    async with msg.channel.typing():
        while filt:
            currFilt = filt[0]
            if not currFilt: 
                filt.pop(0)
                continue
            try: img = {
                "blur": lambda: img.filter(ImageFilter.BLUR),
                "contour": lambda: img.filter(ImageFilter.CONTOUR),
                "detail": lambda: img.filter(ImageFilter.DETAIL),
                "edge_enhance": lambda: img.filter(ImageFilter.EDGE_ENHANCE),
                "edge_enhance_more": lambda: img.filter(ImageFilter.EDGE_ENHANCE_MORE),
                "emboss": lambda: img.filter(ImageFilter.EMBOSS),
                "find_edges": lambda: img.filter(ImageFilter.FIND_EDGES),
                "sharpen": lambda: img.filter(ImageFilter.SHARPEN),
                "smooth": lambda: img.filter(ImageFilter.SMOOTH),
                "smooth_more": lambda: img.filter(ImageFilter.SMOOTH_MORE)
            }[currFilt]()
            except:
                if currFilt.isnumeric():
                    for x in range(int(currFilt)):
                        img = {
                            "blur": lambda: img.filter(ImageFilter.BLUR),
                            "contour": lambda: img.filter(ImageFilter.CONTOUR),
                            "detail": lambda: img.filter(ImageFilter.DETAIL),
                            "edge_enhance": lambda: img.filter(ImageFilter.EDGE_ENHANCE),
                            "edge_enhance_more": lambda: img.filter(ImageFilter.EDGE_ENHANCE_MORE),
                            "emboss": lambda: img.filter(ImageFilter.EMBOSS),
                            "find_edges": lambda: img.filter(ImageFilter.FIND_EDGES),
                            "sharpen": lambda: img.filter(ImageFilter.SHARPEN),
                            "smooth": lambda: img.filter(ImageFilter.SMOOTH),
                            "smooth_more": lambda: img.filter(ImageFilter.SMOOTH_MORE)
                        }[lastFilt]()
                else: return await msg.channel.send(f'Invalid filter: {currFilt}')
            filt.pop(0)
            lastFilt = currFilt
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)
async def pixelColor(msg, content, cmd="pixelcolor"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    if content.split(" ")[0]:
        try: x, y = content.split(" ")
        except: return await msg.channel.send("provide x and y")
    else: return await msg.channel.send("no coords provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.load()
    r, g, *b = img[int(x), int(y)]
    if len(b) > 1:
        a = b[1]
    else: a = 255
    b = b[0]
    os.remove(filename)
    return await msg.channel.send(embed=discord.Embed(title=f'R: {r} G: {g} B: {b} ALPHA: {a}', color=discord.Color.from_rgb(r, g, b)))

async def shrinkImg(msg, content, cmd="shrinkimg"):
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    x = content.split(" ")[0]
    if x:
        try:
            red = int(x)
        except:
            return await msg.channel.send("must be int")
    else: red = 2
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.reduce(red)
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def colorize(msg, content, cmd="colorize"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    blackPoint = 0
    whitePoint = 255
    midPoint = 127
    mid = None
    for op, param in content.opsWithParams({"mid": 3}):
        if "-mid" in content:
            mid = tuple(int(x) for x in param)
        if "-midpoint" in content:
            midPoint = int(param[0])
        if "-blackpoint" in content:
            blackPoint = int(param[0])
        if "-whitepoint" in content:
            whitePoint = int(param[0])
    content = content.split(" ", key=lambda x: int(x) if x else False)
    black = content[0:3]
    white = content[3:6]
    await saveImg(filename, url)
    img = Image.open(filename)
    img = ImageOps.colorize(img.convert("L"), black, white, mid=mid, blackpoint=blackPoint, whitepoint=whitePoint, midpoint=midPoint)
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def resizeImg(msg, content, cmd="resizeimg"):
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    content = content.split(" ")
    width = content[0]
    height = content[1]
    try:
        width = int(width)
        height = int(height)
        if len(content) > 2 and content[-1]:
            x1 = int(content[2])
            y1 = int(content[3])
            x2 = int(content[4])
            y2 = int(content[5])
    except:
        return await msg.channel.send("must be int")
    await saveImg(filename, url)
    img = Image.open(filename)
    try:
        img = img.resize((width, height), box=(x1, y1, x2, y2))
    except:
        img = img.resize((width, height))
    finally:
        img.save(filename)  
        with open(filename, "rb") as i:
            await msg.channel.send(file=discord.File(i, filename=filename))
        os.remove(filename)

async def enhanceImg(msg, content, cmd="enhanceimg"):
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    if content.split(" ")[0]:
        enh = content.split(" ")[0:]
    else: return await msg.channel.send("no filter provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    async with msg.channel.typing():
        while enh:
            currFilt = enh[0]
            if not currFilt:
                enh.pop(0)
                continue
            try:
                filt = currFilt.split(",")[0]
                amnt = currFilt.split(",")[1]
            except:
                filt = currFilt
                amnt = 1
            try: 
                if filt == "autocontrast":
                    img = ImageOps.autocontrast(img.convert("RGB"), cutoff=float(amnt))
                else:
                    i = {
                        "color": ImageEnhance.Color(img),
                        "contrast": ImageEnhance.Contrast(img),
                        "brightness": ImageEnhance.Brightness(img),
                        "sharpness": ImageEnhance.Sharpness(img)
                    }[filt]
                    img = i.enhance(float(amnt))
            except Exception as e:
                print(e)
                return await msg.channel.send(f'Invalid filter: {filt}')
            enh.pop(0)
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def cropImg(msg, content, cmd="crop"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    for op, param in content.opsWithParams({"box": 4}):
        if op == "-box":
            x1, y1, x2, y2 = (int(x) for x in param)
            break
    else: amnt = int(content) if content else 20
    await saveImg(filename, url)
    img = Image.open(filename)
    if "-box" in content.opOps:
        img = img.crop(box=(x1, y1, x2, y2))
    else: img = ImageOps.crop(img, border=amnt)
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def imgBorder(msg, content, cmd="imgborder"):
    content = content[len(cmd) + 2:].split(" ")
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    if content[0] and len(content) != 3:
        amnt = int(content[0])
    else: amnt = 20
    if len(content) > 1 and len(content) != 3:
        r, g, b = content[1:4]
    elif len(content) == 3:
        r, g, b = content[0:3]
    else: r=g=b = 0
    r = int(r)
    g = int(g)
    b = int(b)
    await saveImg(filename, url)
    img = Image.open(filename)
    img = ImageOps.expand(img, border=amnt, fill=(r, g, b))
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def greyscale(msg, content, cmd="greyscale"):
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    img = ImageOps.grayscale(img)
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def imgNoise(msg, content, cmd="imgnoise"):
    content = content[len(cmd) + 2:]
    filename = f'{msg.author.id}.png'
    width, height = content.split(" ")[0:2]
    stdev = content.split(" ")[2]
    img = Image.new("RGB", (int(width), int(height)))
    img = Image.effect_noise((img.width, img.height), int(stdev))
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)
    
async def invert(msg, content, cmd="invert"):
    content = content[len(cmd) + 2:].split(" ")
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    if content[0].isnumeric():
        amnt = int(content[0])
    else: amnt = 0
    await saveImg(filename, url)
    img = Image.open(filename)
    img = ImageOps.solarize(img.convert("RGB"), threshold=amnt) 
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def compileImgs(msg, content, cmd="compileimg"):
    content = Content(content)
    filename1 = f'{msg.author.id}.png'
    filename2 = f'{msg.author.id}2.png'
    await saveImg(filename1, content.split(" ")[0])
    await saveImg(filename2, content.split(" ")[1])
    box = (0, 0)
    alpha = .5
    for op, param in content.opsWithParams({"box": 2}):
        if op == "-box":
            box = tuple(int(x) for x in param)
        elif op == "-alpha":
            alpha = float(param)
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    if "-box" in content.opOps: img1.paste(img2, box=box)
    else: img1 = Image.blend(img1, img2, alpha)
    img1.save(filename1)
    with open(filename1, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename="yes.png"))
    os.remove(filename1)
    os.remove(filename2)

async def imgDiff(msg, content, cmd="imgdiff"):
    content = content[len(cmd) + 2:].split(" ")
    filename1 = f'{msg.author.id}.png'
    filename2 = f'{msg.author.id}2.png'
    await saveImg(filename1, content[0])
    await saveImg(filename2, content[1])
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    diffImg = ImageChops.difference(img1.convert("RGB"), img2.convert("RGB"))
    if diffImg.getbbox():
        diffImg.save(filename1)
    with open(filename1, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename="yes.png"))
    os.remove(filename1)
    os.remove(filename2)

async def lightImg(msg, content, cmd="lightimg"):
    content = content[len(cmd) + 2:].split(" ")
    filename1 = f'{msg.author.id}.png'
    filename2 = f'{msg.author.id}2.png'
    await saveImg(filename1, content[0])
    await saveImg(filename2, content[1])
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    lighterImg = ImageChops.lighter(img1.convert("RGB"), img2.convert("RGB"))
    lighterImg.save(filename1)
    with open(filename1, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename="yes.png"))
    os.remove(filename1)
    os.remove(filename2)

async def darkImg(msg, content, cmd="darkimg"):
    content = content[len(cmd) + 2:].split(" ")
    filename1 = f'{msg.author.id}.png'
    filename2 = f'{msg.author.id}2.png'
    await saveImg(filename1, content[0])
    await saveImg(filename2, content[1])
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    darkerImg = ImageChops.darker(img1.convert("RGB"), img2.convert("RGB"))
    darkerImg.save(filename1)
    with open(filename1, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename="yes.png"))
    os.remove(filename1)
    os.remove(filename2)

async def newImg(msg, content, cmd="newimg"):
    content = content[len(cmd) + 2:].split(" ")
    if "https://" in content:
        content = content.replace(url, '')
    try:
        content[1]
        size = content[0:2]
    except: size = (500, 500)
    if len(content) > 2:
        color = content[2:]
    else: color = [0, 0, 0]
    img = Image.new("RGBA" if len(color) == 4 else "RGB", tuple(int(x) for x in size), tuple(int(x) for x in color))
    img.save(f"{msg.author.id}.png")
    with open(f"{msg.author.id}.png", "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=f"{msg.author.id}.png"))
    os.remove(f"{msg.author.id}.png")

async def rectangle(msg, content, cmd="rectangle"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    content.calcOps()
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        x1, y1, x2, y2 = content.replace("{width}", str(img.width), ret=True).replace("{height}", str(img.height)).split(" ")[0:4]
        FR=FG=FB=FA=OA=OR=OG=OB=width = None
        for op, param in content.opsWithParams({"fill": 3, "outline": 3} if not Rgba else {"fill": 4, "outline": 4}):
            if op == "-fill":
                if not Rgba: FR, FG, FB = param
                else: FR, FG, FB, FA = param
            if op == "-outline":  
                if not Rgba: OR, OG, OB = param
                else: OR, OG, OB, OA = param
            if op == "-width":
                width = param
        if Rgba:
            draw.rectangle([(int(x1), int(y1)), (int(x2), int(y2))], fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)), outline=None if not OR else (int(OR), int(OG), int(OB), int(OA)), width=1 if not width else int(width))
        else:
            draw.rectangle([(int(x1), int(y1)), (int(x2), int(y2))], fill=None if not FR else (int(FR), int(FG), int(FB)), outline=None if not OR else (int(OR), int(OG), int(OB)), width=1 if not width else int(width))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def imgArc(msg, content, cmd="imgarc"):
    content = Content(content)
    content.calcOps()
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        x1, y1, x2, y2 = content.replace("{width}", str(img.width), ret=True).replace("{height}", str(img.height)).split(" ")[0:4]
        startAngle = content.split(" ")[4]
        endAngle = content.split(" ")[5]
        FR=FG=FB=FA=width = None
        for op, param in content.opsWithParams({"fill": 3 if not Rgba else 4}):
            if op== "-fill":
                if not Rgba: FR, FG, FB = param
                else: FR, FG, FB, FA = param
            if op == "-width":
                width = param
        if Rgba: draw.arc([(int(x1), int(y1)), (int(x2), int(y2))], 
                            startAngle, endAngle, 
                            fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)), 
                            width=1 if not width else int(width))
        else: draw.arc([(int(x1), int(y1)), (int(x2), int(y2))], int(startAngle), int(endAngle), fill=None if not FR else (int(FR), int(FG), int(FB)), width=1 if not width else int(width))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def ellipse(msg, content, cmd="ellipse"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        x1, y1, x2, y2 = content.replace("{width}", str(img.width), ret=True).replace("{height}", str(img.height)).split(" ")[0:4]
        FR=FG=FB=FA=OR=OG=OB=OA=width = None
        for op, param in content.opsWithParams({"fill": 3, "outline": 3} if not Rgba else {"fill": 4, "outline": 4}):
            if op == "-fill":
                if not Rgba: FR, FG, FB = param
                else: FR, FG, FB, FA = param
            if "-outline" in params:
                if not Rgba: OR, OG, OB = param
                else: OR, OG, OB, OA = param
            if "-width" in params:
                width = param
        if Rgba: draw.ellipse([(int(x1), int(y1)), (int(x2), int(y2))], outline=None if not OR else (int(OR), int(OG), int(OB), int(OA)), fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)), width=1 if not width else int(width))
        else: draw.ellipse([(int(x1), int(y1)), (int(x2), int(y2))], outline=None if not OR else (int(OR), int(OG), int(OB)), fill=None if not FR else (int(FR), int(FG), int(FB)), width=1 if not width else int(width))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def line(msg, content, cmd="line"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    params = content.split(" ")
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        x1, y1, x2, y2 = content.replace("{width}", str(img.width), ret=True).replace("{height}", str(img.height)).split(" ")[0:4]
        FR=FG=FB=FA=width = None
        for op, param in content.opsWithParams({"fill": 3 if not Rgba else 4}):
            if "-fill" in params:
                if Rgba: FR, FG, FB, FA = param
                else: FR, FG, FB = param
            if "-width" in params:
                width = param
        if Rgba: draw.line([(int(x1), int(y1)), (int(x2), int(y2))], 
                            fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)), 
                            width=1 if not width else int(width))
        else: draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=None if not FR else (int(FR), int(FG), int(FB)), width=1 if not width else int(width))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def point(msg, content, cmd="point"):
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        params = content.split(" ")
        XYS = params[0:]
        FR=FG=FB=OR=OG=OB = None
        if "-fill" in params:
            FR, FG, FB = params[params.index("-fill") + 1 : params.index("-fill") + 4]
            XYS.remove(FR)
            XYS.remove(FG)
            XYS.remove(FB)
            XYS.remove("-fill")
        newXYS = [""]
        for XY in XYS:
            if len(newXYS[-1]) % 2 != 0:
                newXYS[-1].append(int(XY))
            else:
                newXYS.append([int(XY)])
        XYS = [tuple(XY) for XY in newXYS if type(XY) != str]
        draw.point(XYS, fill=None if not FR else (int(FR), int(FG), int(FB)))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def polygon(msg, content, cmd="poly"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        FR=FG=FB=FA=OR=OG=OB=OA = None
        for op, param in content.opsWithParams({"fill": 3, "outline": 3} if not Rgba else {"fill": 4, "outline": 4}):
            if op == "-fill":
                if Rgba: FR, FG, FB, FA = param
                else: FR, FG, FB = param
            elif op == "-outline":
                if Rgba: OR, OG, OB, OA = param
                else: OR, OG, OB = param
        XYS = content[0:].split(" ")
        newXYS = [""]
        for XY in XYS:
            if not XY: continue
            if len(newXYS[-1]) % 2 != 0:
                newXYS[-1].append(int(XY))
            else:
                newXYS.append([int(XY)])
        XYS = [tuple(XY) for XY in newXYS if type(XY) != str]
        if Rgba: draw.polygon(XYS, fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)), outline=None if not OR else (int(OR), int(OG), int(OB), int(OA)))
        else: draw.polygon(XYS, fill=None if not FR else (int(FR), int(FG), int(FB)), outline=None if not OR else (int(OR), int(OG), int(OB)))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def imgText(msg, content, cmd="imgtext"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    await saveImg(filename, url)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        split = content.split(" ")
        if split[0] not in ("center", "top", "bottom"):
            x, y = split[0:2]
        else: 
            x=y = split[0]
            split.insert(1, "center")
        text = Content(" ".join(split[2:]), removeCmd=False)
        fill=FR=FG=FB=direction=txtWidth = None
        font = ImageFont.load_default()
        if msg.attachments:
            text = text.replace(msg.attachments[0].url, "")
        for op, param in text.opsWithParams({"fill": 3, "font": 2}):
            if op == "-fill":
                FR, FG, FB = param
            if op == "-txtwidth":
                txtWidth = param
            if op == "-font":
                font = f'{param[0].title()}.ttf'
                fontSize = int(param[1])
                font = ImageFont.truetype(f"/usr/share/fonts/truetype/msttcorefonts/{font}", fontSize, encoding="unic")
        imgWidth = img.width
        imgHeight = img.height
        text = text.string
        textWidth, textHeight = font.getsize(text)
        if x == "center":
            draw.text(((imgWidth - textWidth) / 2, (imgHeight - textHeight) / 2), text, font=font, fill=(int(FR), int(FG), int(FB)) if FR else None, stroke_width=0 if not txtWidth else txtWidth)
        elif x == "top":
            draw.text(((imgWidth - textWidth) / 2, 0), text, font=font, fill=(int(FR), int(FG), int(FB)) if FR else None, stroke_width=0 if not txtWidth else txtWidth)
        elif x == "bottom":
            draw.text(((imgWidth - textWidth) / 2, imgHeight - textHeight), text, font=font, fill=(int(FR), int(FG), int(FB)) if FR else None, stroke_width=0 if not txtWidth else txtWidth)
        else:
            draw.text((int(x), int(y)), text, font=font, fill=(int(FR), int(FG), int(FB)) if FR else None, stroke_width=0 if not txtWidth else txtWidth)
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def convertImg(msg, content, cmd):
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    mode = content.split(" ")[0]
    pallete=colors = None
    for op, param in content.opsWithParams():
        if op == "-palette":
            pallete = param
        if op == "-colors":
            colors = param
    await saveImg(filename, url)
    img = Image.open(filename)
    if mode == "LAB":
        return await msg.channel.send("PRAISE L A B ")
    img = img.convert(mode=mode, palette=0 if not pallete else pallete, colors=256 if not colors else colors)
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def sortImg(msg, content, cmd="sortimg"):
    content = content[len(cmd) + 2:].split(" ")
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    sortBy = content[0]
    img = Image.open(filename)
    async with msg.channel.typing():
        data = list(img.getdata())
        if sortBy.lower() in ["btw", "ltd"]:
            data.sort(key=lambda x: sum(x))
        elif sortBy.lower() in ["wtb", "dtl"]:
            data.sort(key=lambda x: sum(x), reverse=True)
        elif sortBy.lower() in ["r", "red"]:
            data.sort(key=lambda x: x[0], reverse=True)
        elif sortBy.lower() in ["g", "green"]:
            data.sort(key=lambda x: x[1], reverse=True)
        elif sortBy.lower() in ["b", "blue"]:
            data.sort(key=lambda x: x[2], reverse=True)
        elif sortBy.lower() == "custom":
            source = " ".join(content[1:])
            if not Content(" ".join(content), removeCmd=False).suitibleForEval():
                return await msg.channel.send("nice try")
            code = compile(source, "", "eval")
            data.sort(key=lambda px: eval(code), reverse=True)
        img.putdata(data)
    img.save(filename)  
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

async def imgBand(msg, content, cmd="imgband"):
    content = content[len(cmd) + 2:].split(" ")
    content = " ".join(content[0])
    content = content.split("+")
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    bands = [c.strip() for c in content]
    img = Image.open(filename)
    img = img.convert("RGBA")
    r, g, B, a = img.split()
    band = []
    for b in bands:
        if b.strip() == "r": band.append(r)
        elif b.stripmm() == "g": band.append(g)
        elif b.strip() == 'b': band.append(B)
        elif b.strip() == "a": band.append(a)
    for n, b in enumerate(band):
        b.save(f'{msg.author.id}{n}.png')  
    for n, b in enumerate(band):
        with open(f'{msg.author.id}{n}.png', "rb") as i:
            await msg.channel.send(file=discord.File(i, filename=f'{msg.author.id}{n}.png'))
        os.remove(f'{msg.author.id}{n}.png')

async def ytdl(msg, content, cmd="ytdl"):
    global queue
    song = content[len(cmd) + 2:]
    if song:
        await msg.channel.send("wait 4 years")
        with youtube_dl.YoutubeDL({"format": "bestaudio/best", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]}) as dl:
            dl.download([song])
    for f in os.listdir("./"):
        if f.endswith(".mp3"):
            with open(f, "rb") as mp3:
                return await msg.channel.send(file=discord.File(mp3, "song.mp3"))
            os.remove(f)

async def botMods(msg, content, cmd="botmods"):
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    content = Content(content)
    if content @ "--raw":
        with open(botModsFilePath, "rb") as f:
            return await msg.channel.send(file=discord.File(f, "botmods.json"))
    with open(botModsFilePath, "r") as j:
        data = json.load(j)
        if content:
            try: return await msg.channel.send("\n".join(data.get(str(content.getUser(msg).id))))
            except: return await msg.channel.send("None")
        else: return await msg.channel.send("\n".join([f'{await getUserInContent(msg, "ok " + k, "ok")}: {i}' for k, i in BOTMODS.items()]))

async def embedCmd(msg, content, cmd="embed"):
    content = Content(content)
    color=image=thumbnail=author = None
    title = content.split("|")[0]
    content.replace(f'{title} ', "")
    content = Content(content.split("|", pastIndex=1), removeCmd=False)
    for op, param in content.opsWithParams({"author": (slice(0,None,None), " ")}):
        if op == "-color":
            color = param
        elif op == "-image":
            image = param
        elif op == "-thumbnail":
            thumbnail = param
        elif op == "-author":
            author = Content(" ".join(param), removeCmd=False)
            list(author.opsWithParams())
            author = str(author)
    content.formatMessage(msg, {"{title}": title, "{color}": color, "{author}": author})
    embed = discord.Embed(title=title, color=discord.Color(int(color, 16)) if color else discord.Color(0x000000))
    if image: embed.set_image(url=image)
    if thumbnail: embed.set_thumbnail(url=thumbnail)
    if author: embed.set_author(name=author)
    split = content.split("|")
    for n, field in enumerate(split):
        name, value = field.split(",")
        value = Content(value, removeCmd=False)
        Inline = True if not value @ "--ninline" else False
        embed.add_field(name=name, value=str(value), inline=Inline)
    return await msg.channel.send(embed=embed)

async def emoteUsage(msg, content, cmd="emoteusage"):
    content = Content(content)
    top = 10
    if content @ "--raw":
        with open(emoteUsageFilePath, "rb") as f: return await msg.channel.send(file=discord.File(f, "emoteusage.json"))
    for op, param in content.opsWithParams():
        if op == "-top":
            top = int(param)
            break
    with open(emoteUsageFilePath, "r") as j:
        data = json.load(j)
        data = sorted(data.items(), key=lambda x: x[1], reverse=True if not content @ "--least" else False)
        if content:
            data = {k: i for k, i in data}
            try: usage = data[str(re.findall(r'[0-9]{18}', str(content))[0])]
            except: usage = None
            return await msg.channel.send(usage)
        else:
            emotes = []
            try: 
                File = content @ "--file"
                for n, k in enumerate(data):
                    if n > top and not File: break
                    try: emote = (await msg.guild.fetch_emoji(int(k[0]))).name
                    except discord.errors.NotFound as e: continue
                    emotes.append(f'<:{emote}:{int(k[0])}>: {k[1]}')
                if File: raise FileException("wanted file")
                return await msg.channel.send("\n".join(emotes))
            except Exception as e:
                if not isinstance(e, FileException):
                    await msg.channel.send("too long here's a text file")
                else: await msg.channel.send("file requested")
                with open("EMOTEFILE.txt", "w") as f:
                    for emote in emotes:
                        f.write(f'{emote.split(":")[1]}: {emote.split(":")[-1]}\n')
                with open("EMOTEFILE.txt", "rb") as f:
                    await msg.channel.send(file=discord.File(f, "emoteusage.txt"))
                os.remove("EMOTEFILE.txt")

async def toKelvin(msg, content, cmd="tok"):
    content = Content(content)
    if content[-1] == "f":
        ans = (9 / 5 * float(content[:-1]) + 32) + 273
    elif content[-1] == "c":
        ans = float(content[:-1]) + 273

    return await msg.channel.send(str(ans))

async def guessingGame(msg, content, cmd="guessinggame"):
        c = Content(content)
        Bet = c @ "--bet"
        LOW, HIGH, LIVES = 1, 100, 5
        if len(c) > 0:
            c = c.split(" ")
            HIGH = int(c[0])
            c.pop(0)
            if len(c) >= 1: LIVES = int(c[0])
        STARTLIVES = LIVES
        ans = random.randint(LOW, HIGH)
        await msg.channel.send("guess")
        while True:
            try: c = (await client.wait_for("message", check=lambda mssg: mssg.author == msg.author and (mssg.content.isnumeric() or mssg.content.lower() in ["stop", "giveup", "cancel"]), timeout=60.0)).content.lower()
            except: return await msg.channel.send("waited too long")
            if c in ["stop", "giveup", "cancel"]:
                return await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(100, 0, 0)))
            LIVES -= 1
            if int(c) == ans:
                say = f"YOU WIN\nWITH {LIVES} LIVES LEFT" if not Bet else f'YOU WIN\nWITH {LIVES} LIVES LEFT\nYou earned {(int(ans) // STARTLIVES)}'
                if Bet: await addMoney(msg.author, (int(ans) // STARTLIVES))
                rv = await msg.channel.send(embed=discord.Embed(title=say, color=discord.Color.from_rgb(0, 255, 0)))
                return await embedToReadableDict(rv, rv.embeds[0])
            elif LIVES <= 0:
                say = f"YOU LOSE\nTHE ANSWER WAS {ans}" if not Bet else f'YOU LOSE\nTHE ANSWER WAS {ans}\nYOU LOSE {(int(ans) // STARTLIVES)}'
                if Bet: await addMoney(msg.author, -(int(ans) // STARTLIVES))
                rv = await msg.channel.send(embed=discord.Embed(title=say, color=discord.Color.from_rgb(255, 0, 0)))
                return await embedToReadableDict(rv, rv.embeds[0])
            await msg.channel.send(f"{msg.author.mention} too high" if int(c) > ans else f"{msg.author.mention} too low\nguess\nyou have {LIVES} lives left")