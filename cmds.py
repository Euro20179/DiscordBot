from common import *

async def stop(*args, **kwargs)->None: #similar to how raise StopIteration works, it stops whatever is happening
    global Stop
    Stop = True
    if args: return random.choice(args)

async def hlp(msg, content, cmd="help"):
    global CATS, CMDLIST, CUSTOMCMDS
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    cat = splitContent(content, cmd + " ", index=1).upper()
    File = True if testInContent(cat.lower(), "--file") else False
    if File: 
        cat = cat.replace(" --FILE", "").strip()
    if not cat and "--file" not in cat.lower():
        embed = discord.Embed(title="General", color=discord.Color(0x0000ff))
        with open("cmds.json", "r") as j:
            data = json.load(j)
            for cat in data:
                embed.add_field(name=cat["cat"], value=cat["desc"])
        await msg.channel.send(embed=embed)
        return "help"
    elif cat in CATS:
        embed = discord.Embed(title=cat, color=discord.Color(0x00ffe2))
        if cat == "CUSTOM":
            for cmd in CATS[cat]:
                embed.add_field(name=f'{cmd["name"]}', value=f'``{cmd["name"]}``  {cmd["desc"]}')
        else:
            for cmd in CATS[cat]:
                embed.add_field(name=f'{cmd["name"]}', value=f'``{cmd["name"]}``  {cmd["params"]}', inline=False)
        try:
            if File: raise Exception("file specified") 
            await msg.channel.send(embed=embed)
        except:
            if not cat: cat = "help"
            with open(f'{cat}.txt', "w") as f:
                for cmd in CATS[cat]:
                    f.write(f'{cmd["name"]}  {cmd["params"]}\n\nDescription: {cmd["desc"]}\n\nAliases: {cmd.get("aliases")}\n\n\n\n')
            with open(f'{cat}.txt', "rb") as f:
                await msg.channel.send(file=discord.File(f, f'{cat}.txt'))
            os.remove(f"{cat}.txt")
        return cat

    with open("cmds.json", "rb") as j:
        if testInContent(content, "--all", "--indepth"): #the file
            await msg.channel.send(file=discord.File(j, "cmds.json"))
        else: #by specific commoand
            command = splitContent(content, " ", index=1)
            embed = discord.Embed(title=command, color=discord.Color(0x00ffe2))
            for cmd in CATS.values():
                for c in cmd:
                    if (al := c.get("aliases")):
                        if command in al: isCmd = True
                    else: isCmd = False
                    if c["name"] == command or isCmd:
                        params = c["params"]
                        desc = c["desc"]
                        aliases = c.get("aliases")
                        if aliases: aliases = ",\n".join(f'``{x}``' for x in aliases)
                        text = f'**``{command}``**: ``{params}``\n\n{desc}\n\n__Aliases__:\n{aliases}'
                        break
            try: embed.add_field(name="description", value=text)
            except: return await msg.channel.send('command not found')
            await msg.channel.send(embed=embed)

async def spam(msg, messages, message, BlockStop=False):
    global Stop
    for _ in range(int(messages)):
        if Stop and not BlockStop:
            Stop = False
            return await msg.channel.send(await stop("Stopped"))
        msg = await msg.channel.send(random.choice(message))
        await asyncio.sleep(random.uniform(.7, 1.3))
    return msg

async def ping(msg, content, cmd="ping"):
    if random.random() >= .95:
        await msg.author.send("upupdowndownleftrightleftright")
        await asyncio.sleep(5)
        await msg.author.send("OH SHOOT I WASNT SUPPOSED TO SAY TH-")
        await asyncio.sleep(1)
        await msg.author.send("goodbye")

    if random.random() >= .99:
        return await msg.channel.send("uh yeah tbh i don't really know what this does, like i have an idea but like idk")
    elif random.random() >= .97:
        return await msg.channel.send("LOL GET PRANKD THIS DOES NOTHING ROFL XD XD XD XD XD")
    else: return await msg.channel.send(f':ping_pong: {round(client.latency * 1000)}ms')	

async def echo(msg, content, cmd="echo"):
    print(content, cmd)
    content = content[len(cmd) + 2:]
    try: await msg.delete()
    except: pass
    if "--e" in content:
        c = content.replace(" --e", "")
        embed = discord.Embed(title=c)
        await msg.channel.send(embed=embed)			
        return c
    if random.random() > .99: await msg.author.send("the secret message dm euro for a doubley secret role, if you tell anyone how you got this the role will be taken away\nif you already have the role, you may choose to dm a screenshot of this message to someone, and they have the chance to get the role")	
    return await msg.channel.send(content)

async def timers(msg, content, cmd="timers"):
    embed = discord.Embed(title="Timers")
    with open(timersPath, "r") as tJ:
        data = json.load(tJ)
        for user, t in data.items():
            embed.add_field(name=user, value=round(time.time() - t, 2))
        await msg.chanel.send(embed=embed)
        return f'{user}: {round(time.time() - t, 2)}'

async def levelMessage(msg, content, cmd="lvlmsg"):
    if isBot(msg, client): return await msg.channel.send(await formatLevelMessage(msg, "I AM GREAT I AM LEVEL {level}", 9999999))
    with open(levelingDataFilePath, "r+") as j:
        data = json.load(j)
        changeTo = content[len(cmd) + 2:].strip()
        userData = data[str(msg.author.id)]
        if testInContent(changeTo, "--see", "--get", "--s", "--g"):
            return await msg.channel.send(await formatLevelMessage(msg, userData["message"], userData["level"]))
        Yes = testInContent(changeTo, "--y", "--f")
        if not Yes:
            await msg.channel.send("type y to change message, type n to cancel")
            try: yn = (await client.wait_for('message', check=lambda message: message.author == msg.author, timeout=60.0)).content.lower()
            except asyncio.TimeoutError: yn = "n"
        else: 
            changeTo = changeTo.replace(Yes, "")
            yn = "y"
        if yn in ("yes", "y") or Yes:
            userData["message"] = changeTo
            clearFile(j)
            json.dump(data, j)
            return await msg.channel.send(f"changed to {changeTo}")
        return await msg.channel.send("CANCELLED")

async def cmdUsage(msg, content, cmd="commandusage"):
    top = 10
    if testInContent(content, "-top"):
        top = int(splitContent(content, "-top ")[1].strip())
        content = cmd
    if testInContent(content, "--raw"):
        with open(commandusageFilePath, "rb") as j:
            return await msg.channel.send(file=discord.File(j, commandusageFilePath))
    with open(commandusageFilePath, "r+") as j:
        data = json.load(j)
        if (split := splitContent(content, cmd, index=1).strip()):
            commandUse = data.get(split)
            if not commandUse:
                return await msg.channel.send("command not found")
            embed = discord.Embed(title=split)
            embed.add_field(name="times", value=commandUse)
            await msg.channel.send(embed=embed)
        else:
            data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
            send = "\n".join([f'{n + 1}: {c[0]}, {c[1]}' for n, c in enumerate(data.items()) if n < top])
            try:
                clearFile(j)
                json.dump(data, j) 
                return await msg.channel.send(send)
            except: return await msg.channel.send("too long of a message")
            

async def iq(msg, content, cmd="iq"):
    iq = random.randint(-3, 200)
    c = msg.author.mention if not splitContent(content, f'{cmd} ', index=1) else content[len(cmd) + 2:]
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
    user = await getUserInContent(msg, content, cmd)
    if len(splitContent(content, " ")) > 1:
        user = discord.utils.get(msg.guild.members, id=user.id)
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
    embed.add_field(name="level up mesage", value=await formatLevelMessage(msg, message, level), inline=False)
    await msg.channel.send(embed=embed)
    return f'level: {level}\nxp: {xp}\nrequired: {required}\npos: {pos}\nxp needed: {required - xp}\napprox minutes: {round((required - xp) / 57.5)}\nlevel up message: {await formatLevelMessage(msg, message, level)}'

async def leaderboard(msg, content, cmd="top"):
    if testInContent(content, "--raw"):
        with open(levelingDataFilePath, "rb") as f:
            await msg.channel.send(file=discord.File(f, levelingDataFilePath))
            return "FILE"
    top = 12
    if testInContent(content, " "):
        t = splitContent(content, " ", index=1)
        try: top = int(t)
        except: await msg.channel.send("NaN")
    with open(levelingDataFilePath, "r") as f:
        data = json.load(f)
        users = [(discord.utils.get(msg.guild.members, id=int(user)), int(data[user]["level"]), int(data[user]["xp"])) for user in data.keys()]
        users.sort(key=lambda x: (x[1] * 1000) + (x[2] / 1000), reverse=True)
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
    with open(mballresponseFilePath, "r") as f:
        responses = f.read().split("\n")

    if testInContent(content, "--embed", "--e"):
        return await msg.channel.send(embed=discord.Embed(title=random.choice(responses)))
    return await msg.channel.send(f'Answer: {random.choice(responses)}')

async def spamCmd(msg, content, cmd="spam"):
    global Stop
    if Stop: Stop = False

    c = content[len(cmd) + 2:]

    try: messages = int(c[:c.find(" ")])
    except: return await msg.channel.send("not a valid number of messages")		

    if messages > (lim := random.randint(40000, 110000)):
        return await msg.channel.send(f"pls consult a psychiatrist that's too many messages\nthe limit is: {lim}")		

    if messages < 0: return await msg.channel.send("ERROR: MESSAGE COUNT LESS THAN 0")

    if testInContent(c, "-random"):
        c = c.replace("-random", "")
        c = c[c.find(str(messages)) + len(str(messages)):]
        options = c.split(", ")
        return await spam(msg, int(messages), options)

    message = c[c.find(str(messages)) + len(str(messages)):]
    await spam(msg, messages, [message])
    if random.random() >= .99: await msg.channel.send("You found an easter egg hehe")
    else: return await msg.channel.send(random.choice(("done", "Done")))

async def randomFace(msg, content, cmd="randomface"):
    EYES = (":", ";")
    MOUTHS = (")", "(", "{", "}", "[", "]", "p", "P", "d", "l", "C", "c")
    if random.random() >= .995:
        return await msg.channel.send("()-()\n ___")
    return await oneLineCmd(msg, f'{random.choice(EYES)}{random.choice(MOUTHS)}' if random.random() >= .5 else f'{random.choice(MOUTHS)}{random.choice(EYES)}')

async def alphabet(msg, content, cmd="alphabet"):
    send = string.ascii_lowercase
    if testInContent(content, "--vowels"): send = "aeiou(y)"
    if testInContent(content, "--consonants"):
        send = "".join([x for x in string.ascii_lowercase if x not in "aeiou"])
    if random.random() > .98: send = "zyxwvutsrqponmlkjihgfedcba"
    return await oneLineCmd(msg, send)

async def unicodeChar(msg, content, cmd="unicodechar"):
    amount = 1
    
    sep = splitContent(content, "-sep ", index=1) if testInContent(content, "-sep ") else "\n"

    if (split := splitContent(content, " ")):
        amount = split[1]
        if not isInt(amount): return await msg.channel.send("NaN")
        elif isInt(amount): amount = int(amount)
    chars = [chr(random.randint(0, 185000)) for _ in range(amount)]
    
    return await msg.channel.send(sep.join(chars))

async def serverEmote(msg, content, cmd="serveremote"):
    amount = 1
    sep = "\n"
    if testInContent(content, "-sep"):
        sep = content.split("-sep ")[1]
    if isInt(splitContent(content.lower(), " ", index=1)): amount = int(splitContent(content.lower(), " ", index=1))
    sendE = [str(random.choice(client.emojis)) for _ in range(amount)]
    return await oneLineCmd(msg, sep.join(sendE))

async def writeRoles(msg, content, cmd="doesnothing"):
    filename = splitContent(content.lower(), cmd, index=1)

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
    c = content.split(cmd)[1].strip()
    spaces = c[:c.find(" ")]
    c = c[c.find(" "):]
    if "-sep" in c:
        sep = splitContent(c, "-sep ", index=1)
        c = c.replace(f' -sep {sep}', "")
        if sep == r"\n": sep = "\n"
    if not isInt(spaces):
        return await msg.channel.send(f"{spaces} is not a valid number of spaces")
    add = sep * int(spaces)
    word = add.join(c)
    return await oneLineCmd(msg, word)

async def upperLower(msg, content, cmd="upperlower"):
    mssg = content[len(cmd) + 2:]
    try: await msg.delete()
    except: pass
    else: mssg = mssg.replace(DELETE, "")

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
    setTo = {"r": "rock", "p": "paper", "scissors": "scissors"}
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
            if user2.mention != user1.mention: await addMoney(user2, random.randint(1, 5))
            return await msg.channel.send(f'{user2.mention} WINS')
        elif opps[resp1] == resp2:
            if user2.mention != user1.mention: await addMoney(user1, random.randint(1, 5))
            return await msg.channel.send(f'{user1.mention} WINS')
        else: await msg.channel.send("ITS A DRAW")
    else: await msg.channel.send("either someone spelled something wrong, or someone isn't playing by the rules")

async def complexMessage(msg, content, cmd="complexmessage"):
    c = splitContent(content.lower(), cmd, index=1).split(", ")
    try: await msg.delete()
    except: pass
    try:
        send = c[0].strip().lower()
        filename = c[1]
        mssg = c[2]
    except: await msg.channel.send("make sure you give and seperate each paremeter with a ','")

    dm = (send == "dm")
    send = dm^True

    if cmd == "message": filename = f'{filename}.txt'

    with open(f'.\\message\\{filename}', "w") as f:
        f.write(mssg)
    with open(f'.\\message\\{filename}', 'rb') as f:
        if send: await msg.channel.send(file=discord.File(f, filename))
        if dm:await msg.author.send(file=discord.File(f, filename))

async def sanity(msg, content, cmd="sanity"):
    c = content.split(cmd)[1]

    if testInContent(c, "-r "):
        r = int(content.split("-r ")[1].split(" ")[0])
        c = c.split("-r ")[0]
    else: r = 3

    san = round(random.uniform(-1.5, 101), r)

    cases = {san > 100: f'{c} is so sane that they have become the universe itself',
                san >=49.5 and san <= 50.5: f'{c} is perfectly balanced between sane and insane',
                san < 0: f'how is {c} even alive'}
                
    return await msg.channel.send(cases.get(True)) if cases.get(True) else await msg.channel.send(f'{c} has {san}% sanity')

async def coin(msg, content, cmd="coin"):
    title = res = "heads" if random.random() >= .5 else "tails"
    if testInContent(content, "-bet"):
        bet = splitContent(content, "-bet")[1].strip()
        if bet == "t": bet = "tails"
        if bet == "h": bet = "heads"
        color, title = (0x00ff00, "YOU WIN") if res == bet else (0xff0000, "YOU LOSE")
        if res == bet: 
            add = random.randint(1, 3)
            title += f"\nYOU WON {add}"
            await addMoney(msg.author, add)
        else: 
            add = random.randint(-3, -1)
            title += f'\nYOU LOSE {abs(add)}'
            await addMoney(msg.author, add)
    else:  color = 0xff00ff if res == "heads" else 0x0000ff
    
    embed = discord.Embed(title=title, color=color)
    await msg.channel.send(embed=embed)

async def roleInfo(msg, content, cmd="roleinfo"):
    if not splitContent(content, cmd + " "):
        rolename = msg.author.top_role.name
    else: rolename = splitContent(content, cmd + " ")[1]
    try:
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), msg.guild.roles)
        embed = discord.Embed(title=role.name, color=role.color)
        embed.add_field(name="id", value=role.id)
        embed.add_field(name="Color", value=f'RGB: {", ".join(tuple(str(x) for x in role.color.to_rgb()))}\nHEX: {role.color}')
        embed.add_field(name="displayed seperately?", value=role.hoist)
        embed.add_field(name="hierarchical position", value=len(msg.guild.roles) - role.position)
        embed.add_field(name="members with role", value=len(role.members))
        embed.add_field(name="Created at", value=await formatDateTime(role.created_at))
        await msg.channel.send(embed=embed)
    except AttributeError:
        return await msg.channel.send("role not found")

async def roleCount(msg, content, cmd="rolecount"):
    c = str(content.split(cmd)[1].strip())
    Showroles = False
    if "--showroles" in c:
        Showroles = True
        c = c.replace(" --showroles", "") if c != "--showroles" else ""
    c = c.replace("!", "")[2:-1] if "<@" in c else c
    if not c: c = str(msg.author.id)
    if (m := findMember(c, msg)):
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
    if len(splitContent(content, cmd + " ")) > 1:
        c = content.split(" ")[1:]
        EVEN, ODD = "--even", "--odd"
        Even = True if testInContent(" ".join(c), EVEN) else False
        Odd = True if testInContent(" ".join(c), ODD) else False
        if Even: c.remove(EVEN)
        if Odd: c.remove(ODD)
        low = c[0].strip()
        high = c[1].strip()

        r = int(c[2].strip()) if len(c) == 3 else 15

        if not isInt(r): return await msg.channel.send("you are not rounding to a whole number")				
        if float(low) >= float(high): return await msg.channel.send("Low must be lower than high")

        if isInt(low) and isInt(high):
            while True:
                if Stop: await msg.channel.send(await stop("stopped picking a number"))
                res = random.randint(int(low), int(high))
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
    c = content.split(testInContent(content, "comproles", "compareroles"))[1].split(" ")
    user1 = str(c[1].strip()) 
    user2 = str(c[2].strip())
    if "<@" in user1:
        user1 = str(user1).replace("!", "")[2:-1]
    if "<@" in user2:
        user2 = str(user2).replace("!", "")[2:-1]
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
        return await msg.channel.send("message added")				
    else: return await msg.channel.send("you don't have perms")

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
    try: await msg.delete()
    except: pass
    channel = discord.utils.get(msg.guild.channels, name="counting")
    highest = max([x.content.replace("*", "").replace("_", "").replace("`", "").strip(".") async for x in channel.history(limit=3)])
    highest = int(highest) + 1
    async for x in channel.history(limit=1):
        if x.author == client.user: return ""
    if (style := testInContent(content, "--i", "--b", "--ib", "--e", "--u", "--ui", "--all")):
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
        elif style == "--all":
            await channel.send(f'__***.{highest}.***__')
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
    return await msg.channel.send("\n".join([random.choice(options) for _ in range(int(picks))]))

async def mball(msg, content, cmd="8ball"):
    with open(mballresponseFilePath, "rb") as f:
        await msg.channel.send(file=discord.File(f, "mballresponse.txt"))

async def pigLatin(msg, content, cmd="piglatin"):
    CASE = " --kc"
    content = content.replace(CASE, "") if testInContent(content, CASE) else content.lower()

    m = content.split(" ")[1:]

    if DELETE in m:
        try: await msg.delete()
        except: pass
        m.remove(DELETE)

    for n, word in enumerate(m):
        if word[0] in "aeiou": m[n] += "ay"
        else:
            moveToEnd = [None if letter.lower() in "aeiou" else letter for letter in word] 
            moveToEnd = moveToEnd[:moveToEnd.index(None)] #all the letters until the first vowel represented by None
            m[n] = f'{word[len(moveToEnd):]}{"".join(moveToEnd)}ay'
    return await msg.channel.send(" ".join(m))

async def mostRoles(msg, content, cmd="mostroles"):
    top = int(splitContent(content, " ", index=1)) if splitContent(content, " ", index=1) else 5

    memberRoles = {member.display_name.split("#")[0]: len(member.roles) - 1 for member in msg.guild.members}

    sortedKeys = sorted(memberRoles, key=memberRoles.get, reverse=True)
    top = [f'{r}, {memberRoles[r]}' for n, r in enumerate(sortedKeys) if n < top]
    return await msg.channel.send("\n".join(top))

async def clear(msg, content, cmd="clear"):
    amnt = int(content[len(cmd) + 2:])
    if isBot(msg, client): return msg.channel.send("nope")
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
        return await msg.channel.send("invites cleared")
    else: return await msg.channel.send("you don't have perms")

async def color(msg, content, cmd="color"):
    c = splitContent(content, f'{cmd}')[1].strip()
    if "#" in c:
        color = c.replace("#", "")
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:], 16)
        embed = discord.Embed(title=f'{r} {g} {b}', color=discord.Color(int(color, 16)))
        return await msg.channel.send(embed=embed)
    if ", " in c:
        c = c.replace(" ", "")
        color = [int(x) for x in c.split(",")]
        hexColor = [str(hex(x))[2:] for x in color]
        hexColor = list(map(lambda x: f'0{x}' if len(x) == 1 else x, hexColor))
        return await msg.channel.send(embed=discord.Embed(title=f'#{"".join(hexColor)}', color=discord.Color.from_rgb(color[0], color[1], color[2])))			
    if not c: c = str(msg.author.top_role)
    m = discord.utils.find(lambda r: r.name.lower() == c.lower(), msg.guild.roles)
    if m:
        embed = discord.Embed(title=str(m.color), color=m.color)
        return await msg.channel.send(embed=embed)					
    else: return await msg.channel.send("not a valid role")	

async def serverIcon(msg, content, cmd="servericon"):
    embed = discord.Embed(title="Server icon", color=discord.Colour.from_rgb(180, 70, 180))
    embed.set_image(url=msg.guild.icon_url)
    await msg.channel.send(embed=embed)

async def channelInfo(msg, content, cmd="cc"):
    channel = msg.channel
    embed = discord.Embed(title=channel.name)
    if splitContent(content, cmd)[1]:
        c = content.split(cmd)[1].strip()[2:-1]
        channel = discord.utils.get(msg.guild.channels, id=int(c))
    created = channel.created_at
    diff = datetime.datetime.now() - created
    pinCount = len(await channel.pins())
    if pinCount != 0: daysTillLastPin = (50-pinCount) / (pinCount / int(str(diff).split(" ")[0]))
    embed.add_field(name="Created at", value=await formatDateTime(created))
    embed.add_field(name="Pins", value=pinCount)
    if pinCount != 0: embed.add_field(name="days till last pin", value=str(daysTillLastPin))
    embed.add_field(name="time since creation", value=diff)
    embed.add_field(name="id", value=channel.id)
    embed.add_field(name="position", value=channel.position + 1)
    embed.add_field(name="slowmode delay", value=channel.slowmode_delay)
    embed.add_field(name="mention", value=channel.mention)
    await msg.channel.send(embed=embed)

async def changes(msg, content, cmd="changes"):
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

async def stopwatch(msg, content, cmd="stopwatch"):
    with open(timersPath, "r+") as tJ:
        data = json.load(tJ)
        Running = data.get(str(msg.author.id))
        if not Running:
            data[msg.author.id] = time.time()
            await msg.channel.send(f'{msg.author.mention} stopwatch started')
        elif Running and testInContent(content, "--stop"):
            t = await formatSeconds(time.time() - Running)
            await msg.channel.send(embed=discord.Embed(title=str(round(t[0], 2)) + f' {t[1]}'))
            del data[str(msg.author.id)]
        elif Running and testInContent(content, "-seconds"):
            r = 0 if not splitContent(content, "-seconds ") else int(splitContent(content, "-seconds ")[1])
            t = round(time.time() - Running, r)
            await msg.channel.send(embed=discord.Embed(title=str(t)))
        elif Running:
            t = await formatSeconds(time.time() - Running)
            await msg.channel.send(embed=discord.Embed(title=str(round(t[0], 2)) + f' {t[1]}'))
        clearFile(tJ)
        json.dump(data, tJ)
        

async def emoteInfo(msg, content, cmd="emoteinfo"):
    emote = await msg.guild.fetch_emoji(int(content.split(":")[2][:-1]))
    embed = discord.Embed(title=emote.name)
    embed.add_field(name="Animated", value=emote.animated)
    embed.add_field(name="Added by", value=emote.user)
    embed.add_field(name="created at", value=await formatDateTime(emote.created_at))
    embed.add_field(name="id", value=emote.id)
    await msg.channel.send(embed=embed)

async def messageInfo(msg, content, cmd="messageinfo"):
    sendTo = msg.channel
    content = splitContent(content, f'{cmd} ', index=1).strip()
    fetchFrom = msg.channel
    if msg.channel_mentions:
        fetchFrom = msg.channel_mentions[0]
        content = content.replace(fetchFrom.mention,  "").strip()
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

    await sendTo.send(embed=embed)

async def typeFor(msg, content, cmd="type"):
    timeToType = 5
    if (split := splitContent(content, " ")):
        timeToType = int(split[1])
    if timeToType > 420:
        return await msg.channel.send("sorry thats too long")
    async with msg.channel.typing():
        await asyncio.sleep(timeToType)
    return await msg.channel.send(f'slept for {timeToType} seconds')

async def sendBlank(msg, content, cmd="sendblank"):
    amnt = 5
    if (split := splitContent(content, f"{cmd} ", index=1)):
        amnt = int(split)
    send = "_" + ("\n" * amnt) + "_"
    return await msg.channel.send(send)

async def hangman(msg, content, cmd="hangman"):
    user = (await getUserInContent(msg, content, cmd))
    content = content[len(cmd) + 2:]
    if user.id in playingHangman.keys():
        return await msg.channel.send(f'{msg.author.mention} {user.name} is already in a game')
    if (split := splitContent(content, " ", index=1)): 
        lives = int(split.strip())
    else: lives = 9
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
    embed.add_field(name="roles", value=" ".join([x.mention for x in user.roles]), inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    await msg.channel.send(embed=embed)

async def fetchRole(msg, content, cmd="fetchrole"):
    roleId = int(content[len(cmd) + 2:])
    role = msg.guild.get_role(roleId)
    return await msg.channel.send(role.name)

async def categoryInfo(msg, content, cmd="categoryinfo"):
    content = content[len(cmd) + 2:]
    cat = discord.utils.find(lambda x: x.name.lower() == content.lower(), msg.guild.categories)
    embed = discord.Embed(title=cat.name)
    embed.add_field(name="id", value=cat.id)
    embed.add_field(name="position", value=cat.position)
    embed.add_field(name="channels", value=len(cat.channels))
    embed.add_field(name="text channels", value=len(cat.text_channels))
    embed.add_field(name="voice channels", value=len(cat.voice_channels))
    embed.add_field(name="created at", value=await formatDateTime(cat.created_at))
    await msg.channel.send(embed=embed)

async def spamStop(msg, content, cmd="spamstop"):
    for _ in range(10):
        await msg.channel.send(f'{PREFIX}stop')
        await asyncio.sleep(random.uniform(.3, 1.2))

async def calc(msg, content, cmd="calc"):
    if "help" in content or "quit" in content or "exit" in content or "os." in content:
        return await msg.channel.send('nice try')
    else: return await msg.channel.send(eval(splitContent(content, cmd + " ", index=1)))

async def covid(msg, content, cmd="covid"):
    async with msg.channel.typing():
        request = requests.get("https://www.worldometers.info/coronavirus/")
        embed = discord.Embed(title="Covid Stats", color=discord.Color(0xff0000))
        embed.set_footer(text="source: https://www.worldometers.info/coronavirus/")
        soup = bs.BeautifulSoup(request.text, features="html.parser")
        divs = soup.find_all("div", {"class": "maincounter-number"})
        embed.add_field(name="CASES TOTAL", value=divs[0].text.strip("\n").strip(), inline=False)
        embed.add_field(name="DEATHS TOTAL", value=divs[1].text.strip("\n").strip(), inline=False)
        embed.add_field(name="RECOVERED TOTAL", value=divs[2].text.strip("\n").strip(), inline=False)
        del request
        del soup
        del divs
        await msg.channel.send(embed=embed)

async def pokemon(msg, content, cmd="pokemon"):
    pokemon = splitContent(content, " ", index=1)
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
        await msg.channel.send(embed=embed)
    except Exception as e: 
        print(e)
        return await msg.channel.send("smth went wrong")

async def hypixelPlayerCount(msg, content, cmd="hypixelpc"):
    request = requests.get("https://hypixel.net/")
    soup = bs.BeautifulSoup(request.text, features="html.parser")
    pc = soup.find("div", {"class": "p-header-playNow-count"}).find("b").text
    return await msg.channel.send(pc)
    
async def whoHasRole(msg, content, cmd="hasrole"):
    role = splitContent(content, cmd + " ")[1]
    role = discord.utils.find(lambda r: r.name.lower() == role.lower(), msg.channel.guild.roles)
    embed = discord.Embed(title="has")
    try: 
        has = [user.mention for user in msg.channel.guild.members if role in user.roles]
        embed.add_field(name="has", value="\n".join(has))
        await msg.channel.send(embed=embed)
    except:
        await msg.channel.send("too many chars, here's a text file")
        has = [user.name for user in msg.channel.guild.members if role in user.roles]
        with open(f"whohas{role.name}.txt", "w") as f:
            f.write("\n".join(has))
        with open(f'whohas{role.name}.txt', "rb") as f:
            await msg.channel.send(file=discord.File(f, f'whohas{role.name}.txt'))
        os.remove(f"whohas{role.name}.txt")

async def addCustomCmd(msg, content, cmd="customcmd"):
    global CATS, CMDLIST, CUSTOMCMDS
    c = splitContent(content, ", ")
    name = c[0][len(cmd) + 2:].strip()
    c.pop(0)
    if " " in name: return await msg.channel.send("no spaces in command names")
    say = ", ".join(c)
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for cmd in data:
            if cmd["name"] == name:
                return await msg.channel.send("already a command")
        params = ""
        if "{content}" in say:
            params += " <message>"
        data.append({"name": name, "desc": say, "params": params})
        await msg.channel.send("added")
        clearFile(j)
        json.dump(data, j)
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()

async def removeCustomCmd(msg, content, cmd="removecustomcmd"):
    global CATS, CMDLIST, CUSTOMCMDS
    perms = msg.author.guild_permissions.manage_messages
    if not perms:
        return await msg.channel.send("you cannot do that")
    name = content[len(cmd) + 2:].split()
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for n in name:
            Yes = False
            for cmd in data:
                if cmd["name"] == n:
                    data.remove(cmd)
                    Yes = True
                    break
                if Yes: break
            else: return await msg.channel.send(f"{n} not found")
        clearFile(j)
        json.dump(data, j)
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    return await msg.channel.send(f'removed {" ".join(name)}')

async def deathBattle(msg, users, going, notGoing, responseTime, damageMsgs, healMsgs, embed, first, second):
    global playingDB, Stop
    if Stop: 
        Stop = False
        await removeFromList(playingDB, going, notGoing) 
    tempItems = {item["id"]: item["name"].lower() for item in users[going]["items"]} #gets the items + item ids ready
    temp = await msg.channel.send(f"{going.name} attack or heal\nor item (there is no backing out)") #message to say in chat
    try: #waiting for option
        ah = await client.wait_for("message", check=lambda message: message.author.id == going.id and message.content.lower() in ["attack", "a", "h", "heal", "stop", "item"], timeout=responseTime)
        AH = ah.content.lower()
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
            await msg.channel.send(f"which item (say a number)\n{newLine.join([f'{idd}: {name}' for idd, name in tempItems.items()])}") #says list of items user has
            try:
                i = await client.wait_for("message", check=lambda message: message.author.id == going.id and message.content.lower().isnumeric()) #waits for pick
                i = int(i.content.lower())
            except: #waited too long
                await msg.channel.send("you waited to long, picking 1")
                i = 1
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
    elif AH == f'stop':
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
    await msg.channel.send(embed=embed)
    if users[second]["health"] <= 0 and users[first]["health"] <= 0:
        await removeFromList(playingDB, going, notGoing)
        return await msg.channel.send("ITS A DRAW!")
    if users[second]["health"] <= 0:
        await removeFromList(playingDB, going, notGoing) 
        await addMoney(first, abs(users[second]["health"]))
        return await msg.channel.send(f'{first.name} has won!\nthey earned {abs(users[second]["health"])}')
    elif users[first]["health"] <= 0:
        await removeFromList(playingDB, going, notGoing) 
        await addMoney(second, abs(users[first]["health"]))
        return await msg.channel.send(f'{second.name} has won!\nthey earned {abs(users[first]["health"])}')
    else:
        if going == first:
            await deathBattle(msg, users, second, first, responseTime, damageMsgs, healMsgs, embed, first, second)
        else: await deathBattle(msg, users, first, second, responseTime, damageMsgs, healMsgs, embed, first, second)

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
        if (items := data.get(str(msg.author.id))):
            i1 = items
        else: i1 = []
        if (items := data.get(str(user2.id))):
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
    await msg.channel.send(embed=embed)    
    await deathBattle(msg, users, first, second, responseTime, damageMsgs, healMsgs, embed, first, second)
    
async def mmoney(msg, content, cmd="mmoney"):
    user = await getUserInContent(msg, content, cmd)
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
    buying = splitContent(content, cmd)[1].strip()
    if testInContent(content, ", "):
        split = splitContent(buying, ", ")
        amnt = int(split[1])
        buying = split[0]
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
        if (items := data.get(str(msg.author.id))):
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
    times = 2
    if (t := splitContent(content, " ")[1]).isnumeric():
        times = int(t)
        content = content.replace(f' {str(times)}', "")
    try: return await msg.channel.send(f'{content[len(cmd) + 2:]} '*times)
    except: return await msg.channel.send("message too long, try reducing the number of duplications")

async def customCmdList(msg, content, cmd="customcmdlist"):
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    if testInContent(content, "--raw"):
        with open(customcmdsFilePath, "rb") as f: await msg.channel.send(file=discord.File(f, "customCmds.json"))
    else: 
        try:
            content = await oneLineCmd(msg, "\n".join([f'{x}: {y}' for x, y in CUSTOMCMDS.items()]))
        except:
            with open(customcmdsFilePath, "rb") as f: await msg.channel.send(file=discord.File(f, "customCmds.json"))

async def editCustomCmd(msg, content, cmd="eccmd"):
    lookFor = content.split(", ")[0][len(cmd) + 2:].strip()
    changeTo = content.split(", ")[1:]
    changeTo = ", ".join(changeTo)
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for command in data:
            if command["name"] == lookFor:
                command["desc"] = changeTo
        clearFile(j)
        json.dump(data, j)
    return await msg.channel.send("changed successfully")
