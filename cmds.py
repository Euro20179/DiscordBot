from typing import Mapping
from common import *
from common import __version__

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
    if c.testOps("--all", "--allh"):
        with open('cmds.json', "r") as j:
            data = json.load(j)
        with open(f"help.{'txt' if c @ '--all' else 'html'}", "w", encoding="utf-8") as f:
            if c @ "--all":
                for cat in data:
                    f.write(cat["cat"] + '\n')
                    f.write(cat["desc"] + '\n')
                    for cmd in cat["cmds"]:
                        f.write(f'name: {cmd["name"]}\nparams: {cmd.get("params")}\ndescription: {cmd.get("desc")}\ndate added: {cmd.get("date")}\naliases: {cmd.get("aliases")}\n\n')
            elif c @ "--allh":
                f.write("<html>\n<head>\n<meta charset='utf-8'>\n</head>\n<body style='font-family:arial;font-size:20px;'>")
                for cat in data:
                    f.write(f'<p style="color:red;">{cat["cat"]}</p>')
                    f.write(f'<p style="border-bottom: 1px solid black;color:red;">{cat["desc"]}</p>')
                    for cmd in cat["cmds"]:
                        f.write(f'<p style="border-bottom: 1px dashed black;">name: {cmd["name"]}<br />params: {str(cmd.get("params")).replace("<", "&lt;").replace(">", "&gt;")}<br />description: {cmd.get("desc")}<br />date added: {cmd.get("date")}<br />aliases: {cmd.get("aliases")}<br /></p>')
        with open(f"help.{'txt' if c @ '--all' else 'html'}", "rb") as f:
            mssg = await returnMsg(msg, file=discord.File(f, f"help.{'txt' if c @ '--all' else 'html'}"))
        os.remove(f"help.{'txt' if c @ '--all' else 'html'}")
        return mssg
    for op, param in c.opsWithParams():
        if op == "-added":
            added = param
    cat = str(c).upper()
    if added:
        with open(f'cmds.json', "r") as f:
            data = json.load(f)
            cmds = [cmd["name"] for cat in data for cmd in cat["cmds"] if cmd.get("date") == added]
            return await returnMsg(msg, "\n".join(cmds))
    if not cat:
        embed = discord.Embed(title="General", color=discord.Color(0x0000ff))
        with open("cmds.json", "r") as j:
            data = json.load(j)
            for cat in data:
                embed.add_field(name=cat["cat"], value=cat["desc"])
        return await returnMsg(msg, embed=embed)
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
            if len(embed) > 6000:
                raise Exception("too long")
            return await returnMsg(msg, embed=embed)
        except Exception as e:
            print(e)
            if not cat: cat = "help"
            with open(f'{cat}.txt', "w") as f:
                for cmd in CATS[cat]:
                    f.write(f'{cmd["name"]}\n\nparams: {cmd["params"]}\n\nDescription: {cmd["desc"]}\n\nAliases: {cmd.get("aliases")}\n\nAdded: {cmd.get("date")}\n\n\n\n')
            with open(f'{cat}.txt', "rb") as f:
                return await returnMsg(msg, file=discord.File(f, f'{cat}.txt'))
            os.remove(f"{cat}.txt")
        return cat

    with open("cmds.json", "rb") as j:
        if Raw: #the file
            await returnMsg(msg, file=discord.File(j, "cmds.json"))
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
                return await returnMsg(msg, 'command not found')
            return await returnMsg(msg, embed=embed)

async def spam(msg, messages, message, BlockStop=False):
    global Stop
    for i in range(int(messages)):
        if Stop and not BlockStop:
            Stop = False
            return await returnMsg(msg, await stop("Stopped"))
        send = Content(random.choice(message), removeCmd=False).formatMessage(msg, {"{count}": str(i + 1), "{rcount}": str(int(messages) - i), "{lauthor}": [u.author.name async for u in msg.channel.history(limit=1)][0]}, ret=True)
        msg = await msg.channel.send(str(send))
        await asyncio.sleep(random.uniform(.5, .7))
    return msg

async def ping(msg, content, cmd="ping"):
    """
    gets a bunch of timing statistics
    ping from discord
    time to send message
    time to edit message
    and total execute time
    added: 11/6/19
    """
    startFunction = time.time()
    if random.random() >= .95:
        await msg.author.send("upupdowndownleftrightleftrightba")
        await asyncio.sleep(5)
        await msg.author.send("OH SHOOT I WASNT SUPPOSED TO SAY TH-")
        await asyncio.sleep(1)
        await msg.author.send("goodbye")

    elif random.random() >= .97:
        return await returnMsg(msg, "LOL GET PRANKD THIS DOES NOTHING ROFL XD XD XD XD XD")
    else:
        start = time.time()
        mssg = await msg.channel.send(f'Ping to discord: ``{(client.latency * 1000)}`` ms')
        end = time.time()
        startEdit = time.time()
        await mssg.edit(content=mssg.content + f'\nMessage send time: ``{(end - start) * 1000}`` ms')
        endEdit = time.time()
        await mssg.edit(content=mssg.content + f'\nMessage edit time: ``{(endEdit - startEdit) * 1000}`` ms')
        await mssg.edit(content=mssg.content + f'\nTotal execute time ``{(time.time() - startFunction) * 1000}`` ms')

async def echo(msg, content, cmd="echo"):
    """
    says <message> it and deletes your message
    required params:
        <message>: the message it says
    options:
        -e: makes an embed [color]: gives the embed a color
        -wait <time>: waits time before sedning, still deletes your message instantly
        --dm: dms you
        --nodel: doesn't delete your message
        --tts: uses text to speach
    added: 12/14/19
    """
    c = Content(content)
    c.formatMessage(msg, {"{echo}": Content(content.replace("{echo}", ""))})
    if not c @ "--nodel":
        try: await msg.delete()
        except: pass
    for op, param in c.opsWithParams({"test": (..., '"')}):
        with switch(op) as case:
            if case("-e"):
                if param: color = int(param, 16)
                else: color = 0x000000
                embed = discord.Embed(title=str(c), color=discord.Color(color))
                return await returnMsg(msg, None, embed=embed) if not c @ "--dm" else await returnMsg(msg, None, embed)
            elif case("-wait"):
                try: await asyncio.sleep(float(param))
                except: return await returnMsg(msg, "-wait must be float")
    return await returnMsg(msg, str(c), tts=True if c @ "--tts" else False) if not c @ "--dm" else await returnMsg(msg, str(c), tts=True if c @ "--tts" else False)

async def timers(msg, content, cmd="timers"):
    """
    gets a list of timers that are currently running
    """
    embed = discord.Embed(title="Timers")
    with open(timersPath, "r") as tJ:
        data = json.load(tJ)
        for user, t in data.items():
            embed.add_field(name=user, value=round(time.time() - t, 2))
        return await returnMsg(msg, embed=embed)

async def levelMessage(msg, content, cmd="lvlmsg"):
    """
    when you level up it will say what you give it here
    required params:
        <level message>: the message to set the lvlmsg to
    options:
        --see/--get/--s/--g: shows what will happen when you level up
        --f/--y: automatically agrees to change it
    FORMATS AND {level}, {xp}
    added: 5/29/2020
    """
    if isBot(msg, client): return await returnMsg(msg, "easter e g g")
    changeTo = Content(content).calcOps(rep=True)
    yn = changeTo @ "--y"
    if yn: changeTo.replace("--y", "")
    with open(levelingDataFilePath, "r+") as j:
        data = json.load(j)
        userData = data[str(msg.author.id)]
        if changeTo.testOps("--see", "--get", "--s", "--g"):
            content = Content(userData["message"], removeCmd=False)
            content.formatMessage(msg, {"{level}": userData['level'], "{xp}": userData["xp"]}, removeCmd=False)
            return await returnMsg(msg, str(content))
        if changeTo.testOps("--dontsee"):
            return await returnMsg(msg, "uh, ok then")
        if not yn:
            await msg.channel.send("type y to change message, type n to cancel")
            try: yn = (await client.wait_for('message', check=lambda message: message.author == msg.author, timeout=60.0)).content.lower()
            except asyncio.TimeoutError: yn = "n"
        if yn in ("yes", "y") or yn is True:
            userData["message"] = str(changeTo)
            clearFile(j)
            json.dump(data, j)
            return await returnMsg(msg, f"changed to {changeTo}")
        return await returnMsg(msg, "CANCELLED")

async def cmdUsage(msg, content, cmd="commandusage"):
    """
    gets the usage of each command, top 10 by default
    optional params:
        [command]: the command to see the usage of
    options:
        -top <amount>: the top <amount> of commands
        --least: sorts by least used instead of most used
        --raw: gets the raw json file
    aliases:
        commandusage
        cmdusage
        cmduse
        commanduse
    added: 5/23/2020
    """
    global commandUsage
    content = Content(content)
    top = 10
    with open(commandusageFilePath, "w") as j:
        json.dump(commandUsage, j)
    for op in content.opsWithParams():
        if "-top" == op[0]:
            top = int(op[1])
    if content @ "--raw":
        with open(commandusageFilePath, "rb") as j:
            return await returnMsg(msg, file=discord.File(j, commandusageFilePath))
    with open(commandusageFilePath, "r+") as j:
        data = json.load(j)
        if content and top == 10:
            commandUse = data.get(str(content))
            if not commandUse:
                return await returnMsg(msg, "command not found")
            embed = discord.Embed(title=str(content))
            embed.add_field(name="times", value=commandUse)
            return await returnMsg(msg, embed=embed)
            return await embedToReadableDict(msg, embed)
        else:
            data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=False if content.testOps("--least", "--ltg") else True)}
            send = "\n".join([f'{n + 1}: {c[0]}, {c[1]}' for n, c in enumerate(data.items()) if n < top])
            try:
                clearFile(j)
                json.dump(data, j)
                return await returnMsg(msg, send)
            except: return await returnMsg(msg, "too long of a message")


async def iq(msg, content, cmd="iq"):
    """
    gets the iq of you by default
    optional params:
        [message]: the thing it is getting the iq of
    added: 5/27/2020
    """
    iq = random.randint(-3, 200)
    content = Content(content)
    c = msg.author.mention if not content.split(" ")[0] else str(content)
    await msg.channel.send(f'{c}\'s iq is *DRUMROLL*...')
    await asyncio.sleep(random.uniform(.7, 1.3))
    return await returnMsg(msg, {msg.author.bot: "i am computer i have [ERROR] iq",
            iq == 200: f'you are the next einstein, you are smart enough to realize iq is dumb, so there is no need to say it',
            iq > 150 and iq < 200: f"that's a pretty high iq: {iq}",
            iq > 50 and iq <= 150: iq,
            iq <= 50 and iq >= 0: f"you good there mate, your iq is {iq}",
            iq < 0: f"you literally don't have a brain you somehow have a negative iq idek\nIQ: {iq}"}.get(True))

async def shrug(msg, content, cmd="shrug"):
    """
    shrugs
    added: 5/23/2020
    """
    msg = await msg.channel.send(content=r"¯\_(ツ)_/¯")
    await asyncio.sleep(.3)
    await msg.edit(content=r"¯\\-(ツ)-/¯") ;"THEN"; await asyncio.sleep(.3) ;"THEN"; await msg.edit(content=r"¯\_(ツ)_/¯")
    return msg

async def getUserData(user):
    with open(levelingDataFilePath, "r") as f:
        data = json.load(f)
        return data.get(str(user))

async def level(msg, content, cmd="level"):
    """
    gets your level in the ranking system
    optional params:
        [user]: the user to get the level of
    options:
        --raw: gets the raw json file
    aliases:
        lvl
        rank
        level
    added: 5/22/2020
    """
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
    time, layer = await formatSeconds(((required - xp) / 57.5), layer="minutes")
    embed.add_field(name="approx time", value=f'{round(time, 5)} {layer}') #TODO format this
    embed.add_field(name="level up mesage", value=str(Content(message, removeCmd=False).formatMessage(msg, kwargs={"{level}": level, "{xp}": xp}, removeCmd=False, ret=True)), inline=False)
    return await returnMsg(msg, embed=embed)

async def leaderboard(msg, content, cmd="top"):
    """
    the leaderboard of the highest leveled people
    optional params:
        [top]: the amount of people to show
    options:
        --html: generates an html file instead of an embed (always shows everyone)
    aliases:
        levels
        top
        leaderboard
    added: "5/23/2020
    """
    content = Content(content)
    if content @ "--raw":
        with open(levelingDataFilePath, "rb") as f:
            return await returnMsg(msg, file=discord.File(f, levelingDataFilePath))
    top = 10
    if str(content):
        try: top = int(content)
        except: return await returnMsg(msg, "NaN")
    with open(levelingDataFilePath, "r") as f:
        data = json.load(f)
        users = [(discord.utils.get(msg.guild.members, id=int(user)), int(data[user]["level"]), int(data[user]["xp"]), int(data[user]["required"])) for user in data.keys()]
        users.sort(key=lambda x: (x[1]) + (x[2].__truediv__(x[3] if x[3] > 0 else 99999999999999999999)), reverse=True)
        firstPlaceRole = discord.utils.get(msg.guild.roles, id=713979970287829033)
        if firstPlaceRole not in users[0][0].roles:
            await users[0][0].add_roles(firstPlaceRole)
        if not content @ "--html":
            embed = discord.Embed(title=f"Top {top}", color=users[0][0].color)
            for n, user in enumerate(users):
                if not user[0]: continue
                if firstPlaceRole in user[0].roles and n != 0:
                    await user[0].remove_roles(firstPlaceRole)
                if n > top - 1: break
                embed.add_field(name=str(n + 1), value=f'{user[0].mention}\nLevel: {user[1]}\nXp: {user[2]}')
            return await returnMsg(msg, embed=embed)
        else:
            with open("top.html", "w") as html:
                html.write("<html>\n<head>\n<meta charset='utf-8'><style>p:hover{background-color:#ddd;color:black}\np:active{font-size:2em;}\np {border-bottom: 1px dashed red; color:white;}</style></head><body style='font-family:arial;font-size:20px;background-color:#333'>")
                for n, user in enumerate(users):
                    if user[0]:
                        time, layer = await formatSeconds(((user[3] - user[2]) / 57.5), layer="minutes")
                        html.write(f'<p>{n + 1}: User: {user[0].name} <br />Level: {user[1]} <br /> Xp: {user[2]} <br /> Required: {user[3]} <br /> Xp Needed: {user[3] - user[2]} <br /> Approx time: {time} {layer}')
                html.write("</body>\n</html>")
            with open("top.html", "rb") as html:
                msg = await returnMsg(msg, file=discord.File(html, "top.html"))
            os.remove("top.html")
            return msg

async def magicBall(msg, content, cmd="8ball"):
    """
    the beloved magic 8 ball
    optional params:
        [question]: ask a question (some responses may use it)
    options:
        -e [color]: makes an embed that is black by default or has as color of color
    aliases:
        8
        magicball
        8ball
    added: 5/6/19
    """
    with open(mballresponseFilePath, "r") as f:
        responses = f.read().split("\n")
    choice = Content(random.choice(responses), removeCmd=False)
    choice.formatMessage(msg, {"{question}": str(Content(content))})
    choice._whitespaceFormat()
    for op, param in Content(content).opsWithParams():
        if op == "-e":
            return await returnMsg(msg, embed=discord.Embed(title=choice, color=int(param, 16) if param else 0x000000))
    return await returnMsg(msg, choice)

async def spamCmd(msg, content, cmd="spam"):
    """
    spams <message> over and over again :)
    required params:
        <amount>: the amount of times to spam
        <message>: the message to spam
        OR
        -random *<op> (sep with |): picks randomly from the options seperated by |
    FORMATS AND {count}, {rcount}, {lauthor}
    added: 11/6/2020
    """
    global Stop
    if Stop: Stop = False
    c = Content(content)
    try: messages = int(c.split(" ")[0])
    except: return await returnMsg(msg, "not a valid number of messages")

    lim = random.randint(40000, 110000)
    if messages > lim:
        return await returnMsg(msg, f"pls consult a psychiatrist that's too many messages\nthe limit is: {lim}")

    if messages < 0: return await returnMsg(msg, "ERROR: MESSAGE COUNT LESS THAN 0")

    if "-random" in c:
        c.replace("-random ", "")
        c = " ".join(c.split(" ")[1:])
        options = c.split("|")
        return await spam(msg, int(messages), options)

    message = " ".join(c.split(" ")[1:])
    await spam(msg, messages, [message])
    if random.random() >= .99: await msg.channel.send("You found an easter egg hehe")
    else: return await returnMsg(msg, random.choice(("done", "Done")))

async def randomFace(msg, content, cmd="randomface"):
    """
    generates a random face
    aliases:
        rface
        randface
    """
    BROWS = (">", "|") ;"AND"; EYES = (":", ";") ;"AND"; MOUTHS = (")", "(", "{", "}", "[", "]", "p", "P", "d", "l", "C", "c")
    if random.random() >= .995:
        return await returnMsg(msg, "()-()\n ___")
    if random.random() >= .8:
        return await returnMsg(msg, f'{random.choice(BROWS)}{random.choice(EYES)}{random.choice(MOUTHS)}')
    else:
        return await returnMsg(msg, f'{random.choice(EYES)}{random.choice(MOUTHS)}')

async def alphabet(msg, content, cmd="alphabet"):
    """
    alphabet gives the alphabet
    options:
        -after <letter>: gives only the characters after letter
        -before <letter>: gives only the characters before letter
        -every <amount>: does every <amount> ie: if <amount> is 3 it will do every 3rd character
        --vowels: gives only the vowels
        --consonants: gives only the consonants
        --printable: gives most? of the ascii characters
        --punctuation: gives punctuation
        --oct: octal numbers
        --hex: hexadecimal numbers
        --bin: binary numbers
    aliases:
        alpha
        beta
    added: 5/9/19
    """
    send = string.ascii_lowercase
    content = Content(content)
    with switch(content) as case:
        if case("--vowels"): send = "aeiou(y)"
        elif case("--consonants"): send = "".join([x for x in string.ascii_lowercase if x not in "aeiou"])
        elif case("--printable"): send = string.printable
        elif case("--punctuation"): send = string.punctuation
        elif case("--oct"): send = string.octdigits
        elif case("--hex"): send = "0123456789abcdef"
        elif case("--bin"): send = "01"
    for op, param in content.opsWithParams():
        if op == "-after":
            send = send.split(param)[1]
        elif op == "-before":
            send = send.split(param)[0]
        elif op == "-every":
            send = send[::int(param)]
    if random.random() > .98: send = send[::-1]
    return await returnMsg(msg, send)

async def unicodeChar(msg, content, cmd="unicodechar"):
    """
    generates a random unicode character
    optional params:
        [amount]: the amount of characters to generate
    options:
        -sep <seperator> (WHITESPACEFORMATS): seperates each character by seperator
    added: 11/9/19
    """
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-sep":
            sep = Content.whitespaceFormat(param)
            break
    else: sep = "\n"
    try: amount = int(content)
    except: amount = 1
    return await returnMsg(msg, sep.join([chr(random.randint(0, 185000)) for _ in range(amount)]))

async def serverEmote(msg, content, cmd="serveremote"):
    """
    generates a random custom server emote
    optional params:
        [amount]: the amount of emotes to generate
    options:
        -sep <seperator> (WHITESPACEFORMATS)
    11/9/19
    """
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-sep":
            sep = Content.whitespaceFormat(param)
            break
    else: sep = "\n"
    try: amount = int(content)
    except: amount = 1
    return await returnMsg(msg, sep.join([str(random.choice(client.emojis)) for _ in range(amount)]))

async def writeRoles(msg, content, cmd="doesnothing"):
    """
    does absolutely nothing :)
    required params:
        <text>
    added: 1/1/2020
    """
    filename = Content(content)
    with open(f".\\roles\\{filename}.txt", "w") as f:
        for x in client.get_all_members():
            try: f.write(f'\n{str(x.name)}\n')
            except: f.write(f"\n{x.id}\n")
            for y in x.roles:
                try: f.write(f'{y.name}\n')
                except: f.write(f'{y.id}\n')
    with open(f'{filename}.txt', "rb") as f:
        mssg = await returnMsg(msg, file=discord.File(f, f'{filename}.txt'))
        os.remove(f'{filename}.txt')
        return mssg

async def spacer(msg, content, cmd="spacer"):
    """
    spaces the <message> you give it by <amount>
    required params:
        <message>: the message to space
        <amount>: the amount to space each letter
    options:
        -sep <seperator> (WHITESPACEFORMATS): instead of a space it seperates by seperator
    options:
        --nodel: doesn't delete your message
    """
    sep = " "
    content = Content(content)
    if not content.NoDel:
        try: await msg.delete()
        except: pass
    try: spaces = int(content.split(" ")[0])
    except: spaces = 1
    c = content.split(" ", pastIndex=1)
    if "-sep" in c:
        sep = content.split("-sep ")[1]
        c = c.split("-sep")[0]
        sep = Content.whitespaceFormat(sep)
    add = sep * int(spaces)
    word = add.join(c)
    return await returnMsg(msg, word)

async def upperLower(msg, content, cmd="upperlower"):
    """
    changes your message from:
    "this" to "tHiS"
    required params:
        <message>
    aliases:
        ul
    """
    content = Content(content)
    if not content @ "--nodel":
        try: await msg.delete()
        except: pass
    mssg = content.string
    newPhrase = []

    for val, letter in enumerate(mssg):
        if val > 0:
            if mssg[val - 1] != " " and newPhrase[val - 1].islower():
                letter = letter.upper()
            elif newPhrase[val - 2].islower() and mssg[val - 1] == " ":
                letter = letter.upper()
        newPhrase.append(letter)

    return await returnMsg(msg, "".join(newPhrase))

async def startRPS(msg, content, cmd="rps"):
    """
    play rock paper scissors with <member>
    required params:
        @<member>
    options:
        -time <time>: the amount of time to decide
    aliases:
        rps
        rockpaperscissors
    added: 5/18/2020
    """
    opps = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    setTo = {"r": "rock", "p": "paper", "s": "scissors"}
    t = 15
    if testInContent(content, "-time"):
        t = int(splitContent(content, "-time ", index=1).strip())
        if t >= 120: return await returnMsg(msg, "sorry must be shorter than 2 minutes or 120 seconds")
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
            return await returnMsg(msg, f'{user2.mention} WINS')
        elif opps[resp1] == resp2:
            if user2.mention != user1.mention:
                await addMoney(user2, random.randint(-5, -1))
                await addMoney(user1, random.randint(1, 5))
            return await returnMsg(msg, f'{user1.mention} WINS')
        else: await msg.channel.send("ITS A DRAW")
    else: await msg.channel.send("either someone spelled something wrong, or someone isn't playing by the rules")

async def complexMessage(msg, content, cmd="complexmessage"):
    """
    creates a file if no [.ext] is specified it will be a txt file
    required params:
        <send>: yes/dm, send to chat or dm
        <filename[.ext]>: the file's name, by default is .txt unless .ext is given
        <content>: the content of the file
    options:
        --nodel: doesn't delete your command message
    aliases:
        message
        complexmessage
    added: 1/5/2020?
    """
    content = Content(content)
    if not content @ "--nodel":
        try: await msg.delete()
        except: pass
    content = content.split("|")
    try:
        send = content[0].strip().lower()
        filename = content[1]
        mssg = content[2]
    except: return await returnMsg(msg, "make sure you give and seperate each paremeter with a '|'")
    await writeToFile(msg, mssg, filename, sendMsg=(send == "dm")^True, sendAuthor=(send == "dm"))

async def sanity(msg, content, cmd="sanity"):
    """
    gives the sanity of <mesage>
    requried params:
        <message>
    options:
        -r <round to>: rounds by <round to>, defaults to 3
    added: 1/18/2020
    """
    c = Content(content)
    if "-r" in c:
        r = int(c.split("-r ")[1])
        c = c.split("-r")[0]
    else: r = 2
    san = round(random.uniform(-1.5, 101), r)
    cases = {san > 100: f'{c} is so sane that they have become the universe itself',
                san >=49.5 and san <= 50.5: f'{c} is perfectly balanced between sane and insane',
                san < 0: f'how is {c} even alive'}
    return await returnMsg(msg, cases.get(True)) if cases.get(True) else await returnMsg(msg, f'{c} has {san}% sanity')

async def coin(msg, content, cmd="coin"):
    """
    flips a coin
    optional params:
        [h/t]: bet heads/tails (cannot specify flips if this is chosen)
        [flips]: the amount of times to flip the coin (limit of 10000000)
    added: 1/18/2020
    """
    title = res = "heads" if random.random() >= .5 else "tails"
    if " " in content:
        bet = content.split(" ")[1].strip()
        UseC = "," in bet
        if UseC: bet = bet.replace(",", "")
        if bet == "t": bet = "tails"
        if bet == "h": bet = "heads"
        if not bet.isnumeric() and not UseC:
            color, title = (0x00ff00, "YOU WIN") if res == bet else (0xff0000, "YOU LOSE")
            add = random.randint(1, 3) if res == bet else random.randint(-3, -1)
            await addMoney(msg.author, add)
            title += f'\nYOU WON {add}' if res == bet else f'\nYOU LOSE {abs(add)}'
        elif int(bet) < 10000000:
            heads = 0
            tails = 0
            for _ in range(int(bet)):
                if random.random() > .5: heads += 1
                else: tails += 1
            embed = discord.Embed(title=f'Heads: {format(heads, ",d") if UseC else heads}\nTails: {format(tails, ",d") if UseC else tails}', color=0x00aa00)
            return await returnMsg(msg, embed=embed)
    color = 0xff00ff if res == "heads" else 0x0000ff
    embed = discord.Embed(title=title, color=color)
    return await returnMsg(msg, embed=embed)

async def weightedCoin(msg, content, cmd="weightedcoin"):
    """
    flips a weighted coin
    required params:
        <heads odds>: the odds of landing on heads
    optional params:
        [times]: the times to flip the coin (limit of 10000000)
    added: 6/30/2020
    """
    content = Content(content).split(" ")
    headsOdds = content[0]
    if len(content) > 1:
        flips = content[1]
    else: flips = 1
    UseC = "," in flips
    if UseC: flips = flips.replace(",", "")
    try: headsOdds = float(headsOdds)
    except: return await returnMsg(msg, "not a number")
    if headsOdds > 1 or headsOdds < 0:
        return await returnMsg(msg, "odds must be less than 1 and greater than 0")
    if int(flips) > 1 and int(flips) < 10000000:
        heads = 0
        tails = 0
        for _ in range(int(flips)):
            if random.random() > .5: heads += 1
            else: tails += 1
        embed = discord.Embed(title=f'Heads: {format(heads, ",d") if UseC else heads}\nTails: {format(tails, ",d") if UseC else tails}', color=0x00ff00)
    else:
        ans = "heads" if random.random() <= headsOdds else "tails"
        embed = discord.Embed(title=ans, color=0xff00ff if ans == "heads" else 0x0000ff)
    return await returnMsg(msg, embed=embed)

async def roleInfo(msg, content, cmd="roleinfo"):
    """
    gets info on a role
    optional params:
        [role]: the role to get info on, your top role by default
    added: 5/26/2020
    """
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
        return await returnMsg(msg, embed=embed)
    except AttributeError:
        return await returnMsg(msg, "role not found")

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
            await msg.channel.send(embed=embed)
        else: return await returnMsg(msg, roleCount)
    else: return await returnMsg(msg, "User not found")

async def rand(msg, content, cmd="rand"):
    global Stop
    if Stop: Stop = False
    content = Content(content)
    Even = content @ "--even"
    Odd = content @ "--odd"
    UseC = True if "," in content else False
    content.replace(",", "")
    content = content.split(" ")
    low = 1
    high = 10
    r = 0
    if len(content) > 1:
        r = int(content[2].strip()) if len(content) == 3 else 0
        low, high = float(content[0]), float(content[1])
        try: int(r)
        except: return await returnMsg(msg, "you are not rounding to a whole number")
        if float(low) >= float(high): return await returnMsg(msg, "Low must be lower than high")
    while True:
        if Stop: return await returnMsg(await stop("stopped picking a number"))
        res = random.uniform(low, high)
        if Even and int(round(res, r)) % 2 != 0 and r == 0: continue
        if Odd and int(round(res, r)) % 2 == 0 and r == 0: continue
        else: break
    res = int(round(res, r)) if r == 0 else round(res, r)
    if UseC and not isinstance(res, float):
        res = format(res, ',d')
    return await returnMsg(msg, res)

async def compareRoles(msg, content, cmd="compareroles"):
    embed = discord.Embed(name="Role Comparison")
    c = Content(content)
    u1name = c.getUser(msg, content=c.split("|")[0].strip())
    u2name = c.getUser(msg, content=c.split("|")[1].strip())
    if u1name and u2name:
        roles1 = {role.mention for role in u1name.roles}
        roles2 = {role.mention for role in u2name.roles}
        embed.add_field(name=f'{u1name} role count', value=len(roles1) - 1)
        embed.add_field(name=f'{u2name} role count', value=len(roles2) - 1)
        embed.add_field(name="both members", value="".join(roles1 & roles2), inline=False)
        embed.add_field(name=u1name, value="".join(roles1 - roles2), inline=False)
        embed.add_field(name=u2name, value="".join(roles2 - roles1), inline=False)
        await msg.channel.send(embed=embed)
    else: return await returnMsg(msg, "invalid name(s)")

async def mballreply(msg, content, cmd="mballreply"):
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    mssg = Content(content)
    if str(msg.author.id) in BOTMODS.keys():
        if cmd in BOTMODS[str(msg.author.id)]:
            with open(mballresponseFilePath, "a") as f:
                f.write(mssg + "\n")
            return await returnMsg(msg, "message added")
    else: return await returnMsg(msg, "you don't have perms")

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
                    return await returnMsg(msg, f'removed message: {reply}')
                else: return await returnMsg(msg, "not a message")
    else: return await returnMsg(msg, "you don't have perms")

async def count(msg, content, cmd="count"):
    try: await msg.delete()
    except: pass
    content = Content(content)
    channel = discord.utils.get(msg.guild.channels, name="counting")
    highest = int(max([x.content.replace("*", "").replace("_", "").replace("`", "").strip(".") async for x in channel.history(limit=3)])) + 1
    async for x in channel.history(limit=1):
        if x.author == client.user: return ""
    text = f'.{highest}.'
    fancy = ""
    for op in content.ops():
        if "i" in op:
            fancy += "*"
        if "b" in op:
            fancy += "**"
        if "u" in op:
            fancy += "__"
    if content @ "--all":
        fancy += "***__"
    text = fancy + text + fancy[::-1]
    for op, param in content.opsWithParams():
        if op == "-e":
            if param: color = int(param, 16)
            else: color = 0x000000
            mssg = await channel.send(embed=discord.Embed(title=f'.{highest}.', color=discord.Color(color)))
            break
    else: mssg = await channel.send(text, tts=content @ "--tts")
    if msg.channel != channel: return await returnMsg(msg, mssg.content, embed=mssg.embeds[0] if mssg.embeds else None)

async def choose(msg, content, cmd="choose"):
    content = Content(content)
    opOps = list(content.opsWithParams())
    embed = discord.Embed(title="picks")
    sep = " | "
    picks = 1
    for op, param in opOps:
        if op == "-picks": picks = int(param)
        elif op == "-sep":
            sep = Content.whitespaceFormat(param)
    options = content.split("|", key=lambda x: x.strip())
    return await returnMsg(msg, sep.join([random.choice(options) for _ in range(picks)]))

async def mball(msg, content, cmd="8ball"):
    with open(mballresponseFilePath, "rb") as f:
        return await returnMsg(msg, file=discord.File(f, "mballresponse.txt"))

async def pigLatin(msg, content, cmd="piglatin"):
    content = Content(content)
    if content @ "--kc":
        content = content.lower()
    m = [x for x in content.split(" ") if x]
    for n, word in enumerate(m):
        if word[0] in "aeiou": m[n] += "ay"
        else:
            moveToEnd = [None if letter.lower() in "aeiou" else letter for letter in word]
            if None in moveToEnd: moveToEnd = moveToEnd[:moveToEnd.index(None)] #all the letters until the first vowel represented by None
            m[n] = f'{word[len(moveToEnd):]}{"".join(moveToEnd)}ay'
    return await returnMsg(msg, " ".join(m))

async def mostRoles(msg, content, cmd="mostroles"):
    content = Content(content).split(" ")[0]
    top = int(content) if content else 5
    memberRoles = {member.display_name.split("#")[0]: len(member.roles) - 1 for member in msg.guild.members}
    sortedKeys = sorted(memberRoles, key=memberRoles.get, reverse=True)
    top = [f'{r}, {memberRoles[r]}' for n, r in enumerate(sortedKeys) if n < top]
    return await returnMsg(msg, "\n".join(top))

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
    if isBot(msg, client): return await returnMsg(msg, "nope")
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
        return await returnMsg(msg, "invites cleared")
    else: return await returnMsg(msg, "you don't have perms")

async def color(msg, content, cmd="color"):
    c = Content(content)
    user = c.getUser(msg, 0)
    if user != msg.author:
        color = user.color
        tempColor = str(color)[1:]
        r, g, b = int(tempColor[0:2], 16), int(tempColor[2:4], 16), int(tempColor[4:], 16)
        embed = discord.Embed(title=f'Hex: {str(color)}\nRGB: {r}, {g}, {b}', color=color)
        return await returnMsg(msg, embed=embed)

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
        return await returnMsg(msg, msg, embed=embed)

    if ", " in c:
        c = c.replace(" ", "")
        color = [int(x) for x in c.split(",")]
        hexColor = [str(hex(x))[2:] for x in color]
        hexColor = list(map(lambda x: f'0{x}' if len(x) == 1 else x, hexColor))
        return await returnMsg(msg, embed=discord.Embed(title=f'#{"".join(hexColor)}', color=discord.Color.from_rgb(color[0], color[1], color[2])))

    if not c: c = str(msg.author.top_role)
    m = discord.utils.find(lambda r: r.name.lower() == c.lower(), msg.guild.roles)
    if m:
        embed = discord.Embed(title=str(m.color), color=m.color)
        return await returnMsg(msg, embed=embed)
    else: return await returnMsg(msg, "not a valid role")

async def channelInfo(msg, content, cmd="cc"):
    channel = msg.channel
    content = Content(content).calcOps()
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
    embed.add_field(name="raw mention", value="\\" + channel.mention)
    return await returnMsg(msg, embed=embed)

async def changes(msg, content, cmd="changes"):
    if "--raw" in content:
        with open("CHANGELOG.txt", "rb") as f: return await returnMsg(msg, file=discord.File(f, "CHANGELOG.txt"))
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
            return await returnMsg(msg, "\n".join(vers))
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
                else: return await returnMsg(msg, "did not find version")

            else: c = None

    with open("CHANGELOG.txt", "rb") as f:
        if testInContent(content, "--dms"): return await msg.author.send("\n".join(c)) if c else msg.author.send(file=discord.File(f, "changes.txt"))
        else: return await returnMsg(msg, "\n".join(c)) if c else await returnMsg(msg, file=discord.File(f, "changes.txt"))

async def hexBinOct(msg, content, cmd="hex"):
    content = str(Content(content))
    num = list(map(lambda n: int(n.strip()), content.split("|"))) if "|" in content else [int(content)]
    repWith = {"hex": "0x", "bin": "0b", "oct": "0o", "tobase": ""}[cmd]
    ans = list(map(lambda n: str(hex(n)).replace(repWith, ""), num))
    return await returnMsg(msg, ", ".join(ans))

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
                return await returnMsg(msg, "you cannot go above 100k")
            break
    mssg = str(content).strip()
    async with msg.channel.typing():
        hist = [m.content async for m in msg.channel.history(limit=limit)]
        responses = [hist[n - 1] for n, message in enumerate(hist) if message == mssg]
        if responses: return await returnMsg(msg, f'{msg.author.mention} I HAVE FOUND A RESPONSE\n{random.choice(responses)}')
        else: return await returnMsg(msg, f'did not find {mssg} in the past {limit} messages in this channel')

async def stopwatch(msg, content, cmd="stopwatch"):
    content = Content(content)
    with open(timersPath, "r+") as tJ:
        data = json.load(tJ)
        running = data.get(str(msg.author.id))
        stopAt = content.toSet() & {"seconds", "minutes", "hours", "days", "weeks"}
        if not running:
            data[msg.author.id] = time.time()
            return await returnMsg(msg, f'{msg.author.mention} stopwatch started')
        elif running and content @ "--stop":
            t = await formatSeconds(time.time() - running)
            await msg.channel.send(embed=discord.Embed(title=str(round(t[0], 2)) + f' {t[1]}'))
            del data[str(msg.author.id)]
            return await returnMsg(msg, "timer stopped")
        elif stopAt:
            stopAt = list(stopAt)[0]
            t, layer = await formatSeconds(time.time() - running, stopAt=stopAt)
            r = 15 if not splitContent(content, f'{stopAt} ', index=1) else int(content.split(f'{stopAt} ')[1])
            t = round(t, r)
            return await returnMsg(msg, embed=discord.Embed(title=f'{t} {layer}'))
        elif running:
            t = await formatSeconds(time.time() - running)
            return await returnMsg(msg, embed=discord.Embed(title=str(round(t[0], 2)) + f' {t[1]}'))
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
    return await returnMsg(msg, embed=embed)

async def messageInfo(msg, content, cmd="messageinfo"):
    sendTo = msg.channel
    content = Content(content)
    fetchFrom = msg.channel
    if msg.channel_mentions:
        fetchFrom = msg.channel_mentions[0]
        content = Content(content.replace(fetchFrom.mention,  "").strip(), removeCmd=False)
    if content.string.isnumeric():
        try: msg = await fetchFrom.fetch_message(content)
        except discord.errors.NotFound:
            return await returnMsg(msg, "sorry that message wasn't found")
    embed = discord.Embed(title="message info")
    embed.add_field(name="is tts", value="¯\_(ツ)_/¯")
    embed.add_field(name="author", value=msg.author.mention)
    if msg.content: embed.add_field(name="content", value=msg.content)
    else: embed.add_field(name="files", value="some i guess")
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

    return await returnMsg(msg, embed=embed)

async def typeFor(msg, content, cmd="type"):
    content = Content(content)
    Send = not content @ "--nosend"
    timeToType = float(content.strip()) if content.strip() else 5
    if timeToType > 420:
        return await returnMsg(msg, "sorry thats too long")
    async with msg.channel.typing():
        await asyncio.sleep(timeToType)
    return await returnMsg(msg, f'typed for {timeToType} seconds') if Send else msg

async def sendBlank(msg, content, cmd="sendblank"):
    content = Content(content)
    amnt = int(content) if content else 5
    return await returnMsg(msg, "_" + ("\n" * amnt) + "_")

async def hangman(msg, content, cmd="hangman"):
    content = Content(content)
    user = content.getUser(msg, 0)
    if user.id in playingHangman.keys():
        return await returnMsg(msg, f'{msg.author.mention} {user.name} is already in a game')
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
    except: return await returnMsg(msg, "user did not respond in 1.5 minutes")

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
    return await returnMsg(msg, embed=embed)

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
    embed.add_field(name="raw mention", value="\\" + user.mention)
    embed.add_field(name="roles", value=" ".join([x.mention for x in user.roles]), inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    await msg.channel.send(embed=embed)

async def fetchSomething(msg, content, cmd="fetchrole"):
    content = Content(content)
    func = {"fetchrole": msg.guild.get_role,
    "fetchuser": client.fetch_user,
    "fetchchannel": client.fetch_channel,
    "fetchemote": msg.guild.fetch_emoji}[content.cmd[1:]]
    await func(int(content.split(" ")[0]))
    fetches = [(await func(int(x.strip()))).name for x in content.split(" ")]
    return await returnMsg(msg, "\n".join(fetches))

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
    return await returnMsg(msg, embed=embed)

async def spamStop(msg, content, cmd="spamstop"):
    for _ in range(10):
        await msg.channel.send(f'{PREFIX}stop')
        await asyncio.sleep(random.uniform(.3, 1.2))

async def calc(msg, content, cmd="calc", ReturnRes=False):
    content = Content(content)
    if not content.suitibleForEval():
        return await returnMsg(msg, 'nice try')
    else:
        if str(content) in ["1 + 1", "1+1"]:
            return await returnMsg(msg, "1 + 1 = window")
        elif str(content) in ["2 + 2", "2+2"]:
            return await returnMsg(msg, "2 + 2 = fish")
        try:
            rv = eval(str(content))
            if not ReturnRes: return await returnMsg(msg, rv)
            else: return rv
        except Exception as e:
            print(e)
            return await returnMsg(msg, str(type(e)).split(' ')[1].split("'")[1].strip("'"))

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
        return await returnMsg(msg, embed=embed)
    except Exception as e:
        print(e)
        return await returnMsg(msg, "smth went wrong")

async def hypixelPlayerCount(msg, content, cmd="hypixelpc"):
    game = Content(content).string
    if game:
        data = requests.get(f"https://api.hypixel.net/gameCounts?key={HPKEY}").json()
        if game == "list":
            return await returnMsg(msg, ", ".join(list(x.lower() for x in data["games"].keys())))
        gameData = data["games"].get(game.upper())
        if gameData:
            embed = discord.Embed(title=game, color=discord.Color(0xffff00))
            embed.add_field(name=game, value=gameData["players"])
            modes = gameData.get("modes")
            if modes:
                for mode in modes.items():
                    embed.add_field(name=mode[0], value=mode[1])
            return await returnMsg(msg, embed=embed)
    return await returnMsg(msg, requests.get(f"https://api.hypixel.net/playercount?key={HPKEY}").json()["playerCount"])

async def hypixelBanStats(msg, content, cmd="hypixelban"):
    data = requests.get(f"https://api.hypixel.net/watchdogstats?key={HPKEY}").json()
    embed = discord.Embed(title="ban stats", color=discord.Color(0xffff00))
    for k, v, in data.items():
        if k == "success": continue
        else: embed.add_field(name=k, value=v)
    return await returnMsg(msg, embed=embed)

async def whoHasRole(msg, content, cmd="hasrole"):
    role = Content(content)
    Raw = False if not role @ "--file" else True
    role = discord.utils.find(lambda r: r.name.lower() == role.lower().strip(), msg.channel.guild.roles)
    if not role: return await returnMsg(msg, "role not found")
    has = [user.mention for user in msg.channel.guild.members if role in user.roles]
    try:
        if Raw: raise FileException("wanted file")
        embed = discord.Embed(title=role.name, color=role.color)
        embed.add_field(name="has", value="\n".join(has))
        if len(embed) >= 1024: raise Exception("too long")
        return await returnMsg(msg, embed=embed)
    except Exception as e:
        if not has:
            return await returnMsg(msg, f'no one has {role.name}')
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
    if " " in name: return await returnMsg(msg, "no spaces in command names")
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for cmd in data:
            if cmd["name"] == name:
                return await returnMsg(msg, "already a command")
        params = ""
        if "{content}" in say:
            params += " <message>"
        if datetime.datetime.now().strftime("%Y") == "2020":
            d = datetime.datetime.now().strftime("%m/%d/%Y")
        else:
            d = datetime.datetime.now().strftime("%m/%d/%y")
        data.append({"name": name, "desc": say, "params": params, "date": d, "Locked": Locked, "addedby": str(msg.author.id), "editedby": []})
        mssg = await returnMsg(msg, "added")
        clearFile(j)
        json.dump(data, j)
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    return mssg

async def removeCustomCmd(msg, content, cmd="removecustomcmd"):
    global CATS, CMDLIST, CUSTOMCMDS
    perms = msg.author.guild_permissions.manage_messages
    if not perms and str(msg.author.id) not in BOTMODS.keys():
        return await returnMsg(msg, "you cannot do that")
    name = content[len(cmd) + 2:].split(" ")
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for cmd in data:
            if cmd["name"] in name:
                if cmd.get("Locked"):
                    try:
                        await msg.channel.send(f"{msg.author.mention} this command is locked are you sure")
                        YN = await client.wait_for("message", check=lambda message: message.author.id == msg.author.id, timeout=60.0)
                    except:
                        return await returnMsg(msg, "cancelled")
                    if YN.content.lower() in ["no", "cancel", 'stop', 'n']:
                        return await returnMsg(msg, "cancelled")
                data.remove(cmd)
                name.remove(cmd["name"])
        if name: return await returnMsg(msg, f"{', '.join(name)} not found")
        clearFile(j)
        json.dump(data, j)
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    return await returnMsg(msg, f'removed {" ".join(name)}')

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
            damage = round(random.gauss(-24 + users[going]["healstreak"], 5), 0)
            await temp.delete()
        users[going]["healstreak"] += 1
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
    if CustomMessage:
        users[going]["healstreak"] = 0
        move = CustomMessage
    elif damage > 0:
        users[going]["healstreak"] = 0
        move = random.choice(damageMsgs).replace("{attaker}", going.mention).replace("{aked}", notGoing.mention).replace("{damage}", str(damage))
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
        return await returnMsg(msg, f'{msg.author.name} is in a game')
    if user2 in playingDB:
        return await returnMsg(msg, f'{user2.name} is in a game')
    if msg.author == client.user or user2 == client.user:
        return await returnMsg(msg, "I cannot play sadly :((((((")
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
    users = {msg.author: {"user": msg.author, "health": 100 + b1, "items": i1, "healstreak": 0},
             user2: {"user": user2, "health": 100 + b2, "items": i2, "healstreak": 0}}
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
        return await returnMsg(msg, f'{user.name} has €{data.get(str(user.id))}')

async def shop(msg, content, cmd="shop"):
    with open(itemsFilePath, "r") as j:
        data = json.load(j)
        embed = discord.Embed(title="Items", color=discord.Color(0x00ff00))
        for item in data:
            embed.add_field(name=f'{item["id"]}: {item["name"]}', value=f'Description: {item["desc"]}\nCost: €{item["cost"]}')
        return await returnMsg(msg, embed=embed)

async def buyItem(msg, content, cmd="buyitem"):
    buying = Content(content).string
    if ", " in content:
        amnt = int(buying.split(", ")[1])
        buying = buying.split(", ")[0]
    else: amnt = 1
    with open(moneyDataFilePath, "r") as j:
        data = json.load(j)
        money = data.get(str(msg.author.id))
        if not money: return await returnMsg(msg, "you have no money")
    with open(itemsFilePath, "r") as j:
        data = json.load(j)
        for item in data:
            if item["name"].lower() == buying.lower() or str(item["id"]) == buying:
                forPurchase = item; break
        else: return await returnMsg(msg, "did not find item")
    amountBought = 0
    for _ in range(amnt):
        if money < forPurchase["cost"]: return await returnMsg(msg, "you don't have enough money")
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
    return await returnMsg(msg, f'bought {forPurchase["name"]}')

async def inventory(msg, content, cmd="inv"):
    content = Content(content)
    user = content.getUser(msg)
    with open(itemDataFilePath, "r+", encoding="utf-8-sig") as j:
        data = json.load(j)
        items = data.get(str(user.id))
        if items:
            embed = discord.Embed(name=f"{user.name}'s inventory", color=user.color)
            s = {item["name"] for item in items}
            count = {item: 0 for item in s}
            used = []
            for item in items: count[item["name"]] += 1
            for item in items:
                if item in used:
                    continue
                used.append(item)
                embed.add_field(name=f'{item["name"]} * {count[item["name"]]}', value=f'{item["name"]}: {item["desc"]}',)
            return await returnMsg(msg, embed=embed)
        else: return await returnMsg(msg, "none")

async def duplicator(msg, content, cmd="duplicator"):
    t = Content(content)
    times = 2
    for op, param in t.opsWithParams():
        if op == "-sep":
            sep = Content.whitespaceFormat(param)
            t = Content(t.strip(), removeCmd=False)
            break
    else: sep = " "
    if t.split(" ")[0].isnumeric():
        times = int(t.split(" ")[0])
        t = t.replace(f'{times}', "").string.strip()
    try: return await returnMsg(msg, f'{t}{sep}'*times)
    except: return await returnMsg(msg, "message too long, try reducing the number of duplications")

async def customCmdList(msg, content, cmd="customcmdlist"):
    _, _, CUSTOMCMDS = await reloadCMDSLIST()
    content = Content(content)
    if content @ "--raw":
        with open(customcmdsFilePath, "rb") as f: await msg.channel.send(file=discord.File(f, "customCmds.json"))
    else:
        try:
            if content @ "--file": raise FileException("wanted file")
            content = await msg.channel.send("\n".join([f'{x}: {y}' for x, y in CUSTOMCMDS.items()]))
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
                if command.get("Locked"):
                    if not await hasPerms(str(msg.author.id), cmd) and not str(msg.author.id) == command.get("addedby"):
                        return await returnMsg(msg, "cannot change that command it's locked")
                if "--lock" in changeTo:
                    if not command.get("Locked"):
                        command["Locked"] = True
                    else: command["Locked"] ^= True
                else:
                    command["desc"] = changeTo
                if command.get("editedby"):
                    if str(msg.author.id) not in command["editedby"]:
                        command["editedby"] += [str(msg.author.id)]
                else: command["editedby"] = [str(msg.author.id)]
                break
        else: return await returnMsg(msg, "command doesn't exist")
        clearFile(j)
        json.dump(data, j)
    return await returnMsg(msg, "changed successfully")

async def luckynumber(msg, content, cmd="luckynumber"):
    content = Content(content)
    who = msg.author.mention
    count = 3
    for op, param in content.opsWithParams():
        if op == "-c":
            try: count = int(param)
            except: return await returnMsg(msg, "amount of numbers must be an integer")
    if content: who = content
    nums = " ".join([str(random.randint(1, 10)) for _ in range(count)])
    if random.random() >= .999: return await returnMsg(msg, f"{who}'s lucky numbers are 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7")
    return await returnMsg(msg, f"{who}'s lucky numbers are {nums}")

async def uptime(msg, content, cmd="uptime"):
    content = Content(content)
    stopAt = content.toSet() & {"seconds", "minutes", "hours", "days", "weeks"}
    if stopAt:
        stopAt = tuple(stopAt)[0]
        t, layer = await formatSeconds(time.time() - UPTIME, stopAt=stopAt)
        r = 15 if not splitContent(str(content), stopAt + " ") else int(splitContent(str(content), f'{stopAt} ')[1])
        return await returnMsg(msg, f'{round(t, r)} {layer}')
    else:
        if random.random() > .99: return await returnMsg(msg, "tbh i forget how long i've been on for sorry, i might remember later though")
        t, layer = await formatSeconds(time.time() - UPTIME)
        return await returnMsg(msg, f'{str(t)} {layer}')

async def editCmd(msg, content, cmd="edit"):
    content = Content(content)
    sep = ""
    content.formatMessage(msg)
    sleepFor = .7
    for op, param in content.opsWithParams():
        if op == "-t" or op == "-time":
            if param == "instant":
                sleepFor = 0
            else:
                sleepFor = float(param)
                if sleepFor < 0:
                    return await returnMsg(msg, "must be greater than 0")
        elif op == "-sep":
            sep = Content.whitespaceFormat(param)
    content._whitespaceFormat()
    edits = content.split("|")
    editable = await msg.channel.send(edits[0])
    while edits:
        edits.pop(0)
        if not edits: break
        await asyncio.sleep(sleepFor)

        tokens = {
            "+": "add",
            "-": False,
            "*": "multiply",
            "<": "insertBeggining",
            "%": "replace",
            "^": "insert",
            ";": "newmessage"
        }
        token = tokens.get(edits[0][0])
        if token == None or token == "add": await editable.edit(content=editable.content + f'{sep}{edits[0]}')
        elif token == "multiply": await editable.edit(content=editable.content*int(edits[0][1:]))
        elif token == "replace":
            rep = edits[0].split("%")[1].split(">>")[0]
            repWith = edits[0].split(">>")[1]
            await editable.edit(content=editable.content.replace(rep if rep != "MSG" else editable.content, repWith))
        elif token == "insert":
            pos = edits[0].split("^")[1]
            splitW = "<<" if "<<" in pos else "="
            pos = pos.split(splitW)[0]
            repWith = edits[0].split(splitW)[1]
            foo = Content(editable.content, removeCmd=False)
            if splitW == "<<":
                foo.insert(int(pos), repWith)
            else: foo[int(pos)] = repWith
            await editable.edit(content="".join(foo))
        elif token == "insertBeggining" and edits[0][1] == "<":
            await editable.edit(content=f'{edits[0][2:]}' + editable.content)
        elif token == "newmessage":
            send = Content(edits[0].split(";")[1], removeCmd=False)
            if send @ "--delete":
                await editable.delete()
            editable = await editable.channel.send(send)

        else: await editable.edit(content=editable.content.replace(edits[0][1:], ""))

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
        return await returnMsg(msg, f'response will happen when you are {" ".join(data[str(msg.author.id)]["when"])}')
    return await returnMsg(msg, f"changed to:\n{response}")

async def setStatus(msg, content, cmd="status"):
    st = Content(content)
    if len(st) >= 1:
        await client.change_presence(activity=discord.Game(name=str(st)))
        return await returnMsg(msg, f"changed to {st}")
    else: return await returnMsg(msg, "you didn't set the status to anything")

async def imageInfo(msg, content, cmd="imginfo"):
    att, *_ = await getImg(msg)

    embed = discord.Embed(title=att.filename if att.filename else "UNKNOWN.img")
    embed.add_field(name="id", value=att.id if att.id else "UNKOWN")
    embed.add_field(name="file size", value=att.size if att.size else "UNKOWN")
    embed.add_field(name="width", value=att.width if att.width else "UNKOWN")
    embed.add_field(name="height", value=att.height if att.height else "UNKOWN")
    embed.add_field(name="url", value=att.url if att.url else "UNKOWN")
    embed.add_field(name="spoiler?", value=att.is_spoiler if type(att.is_spoiler) is bool else "UNKNOWN")
    return await returnMsg(msg, embed=embed)

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
    mssg = await returnMsg(msg, embed=embed)
    os.remove(filename)
    return mssg

async def textInfo(msg, content, cmd="textinfo"):
    text = Content(content)
    Re = False
    sep = " "
    for op, param in text.opsWithParams():
        if op in ("-re", "-regex"):
            Re = True
    try:
        _, filename, url = await getImg(msg, NotFromChat=True)
        await saveImg(filename, url)
        with open(filename, "r") as f:
            text = Content(f.read(), removeCmd=False)
    except:
        pass
    if Re:
        find = re.findall(str(param), str(text))
        try: return await returnMsg(msg, sep.join(find))
        except Exception as e:
            print(e)
            if type(e) is discord.errors.HTTPException:
                if not find:
                    return await returnMsg(msg, "did not find any match")
                else:
                    with open("match.txt", "w") as f:
                        f.write(sep.join(find))
                    with open("match.txt", "rb") as f:
                        return await returnMsg(msg, "message too long", file=discord.File(f, "match.txt"))
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
            return await returnMsg(msg, send)
        except:
            with open(f'{msg.author.id}.txt', "w") as f:
                f.write(send)
            with open(f'{msg.author.id}.txt', "rb") as f:
                return await returnMsg(msg, file=discord.File(f, "text.txt"))
            os.remove(f'{msg.author.id}.txt')
    return await returnMsg(msg, embed=embed)

async def embedInfo(msg, content, cmd="embedtotext"):
    content = Content(content).string
    fetchFrom = msg.channel
    if msg.channel_mentions:
        fetchFrom = msg.channel_mentions[0]
        content = content.replace(fetchFrom.mention,  "").strip()
    if content.isnumeric():
        try: embed = (await fetchFrom.fetch_message(content)).embeds[0]
        except discord.errors.NotFound:
            return await returnMsg(msg, "sorry that message wasn't found")
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
            return await returnMsg(msg, 'no messages with embeds found')
    return await returnMsg(msg, (await embedToReadableDict(msg, embed)).content)

async def rotateImg(msg, content, cmd="rotateImg"):
    content = Content(content)
    att, filename, url = await getImg(msg)
    Fit = True if not content @ "--nofit" else False
    if "https://" in content:
        content.replace(url, '')
    if len(content.split(" ")) == 1 and any(content.split(" ")):
        angle = int(content.split(" ")[0])
    else: angle = 90

    if not url: return await returnMsg(msg, "no img provided")
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
    else: return await returnMsg(msg, "no filter provided")
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
                else: return await returnMsg(msg, f'Invalid filter: {currFilt}')
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
        except: return await returnMsg(msg, "provide x and y")
    else: return await returnMsg(msg, "no coords provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.load()
    r, g, *b = img[int(x), int(y)]
    if len(b) > 1:
        a = b[1]
    else: a = 255
    b = b[0]
    os.remove(filename)
    return await returnMsg(msg, embed=discord.Embed(title=f'R: {r} G: {g} B: {b} ALPHA: {a}', color=discord.Color.from_rgb(r, g, b)))

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
            return await returnMsg(msg, "must be int")
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
        return await returnMsg(msg, "must be int")
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
    else: return await returnMsg(msg, "no filter provided")
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
                return await returnMsg(msg, f'Invalid filter: {filt}')
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
        x1, y1, x2, y2 = content.replace("{width}", str(img.width)).replace("{height}", str(img.height)).string.split(" ")[0:4]
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
    content = Content(content).calcOps()
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
        x1, y1, x2, y2 = content.replace("{width}", str(img.width)).replace("{height}", str(img.height)).split(" ")[0:4]
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
        x1, y1, x2, y2 = content.replace("{width}", str(img.width)).replace("{height}", str(img.height)).string.split(" ")[0:4]
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
        x1, y1, x2, y2 = content.replace("{width}", str(img.width)).replace("{height}", str(img.height)).string.split(" ")[0:4]
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
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        FR=FG=FB=OR=OG=OB = None
        for op, param in content.opsWithParams({"fill": 3}):
            if op == "-fill":
                FR, FG, FB = param
        newXYS = [""]
        for XY in content.strip().split(" "):
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
    content = Content(content)
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
        elif b.strip() == "g": band.append(g)
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
    song = Content(content).string
    if song:
        await msg.channel.send("wait 4 years")
        with youtube_dl.YoutubeDL({"format": "bestaudio/best", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]}) as dl:
            dl.download([song])
    for f in os.listdir("./"):
        if f.endswith(".mp3"):
            with open(f, "rb") as mp3:
                rv = await returnMsg(msg, file=discord.File(mp3, "song.mp3"))
            os.remove(f)
            await giveAchievements(msg, "pirate")
            return rv

async def botMods(msg, content, cmd="botmods"):
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    content = Content(content)
    if content @ "--raw":
        with open(botModsFilePath, "rb") as f:
            return await returnMsg(msg, file=discord.File(f, "botmods.json"))
    with open(botModsFilePath, "r") as j:
        data = json.load(j)
        if content:
            try: return await returnMsg(msg, "\n".join(data.get(str(content.getUser(msg).id))))
            except: return await returnMsg(msg, "None")
        else: return await returnMsg(msg, "\n".join([f'{await getUserInContent(msg, "ok " + k, "ok")}: {", ".join(i)}' for k, i in BOTMODS.items()]))

async def embedCmd(msg, content, cmd="embed"):
    content = Content(content)
    color=image=thumbnail=author = None
    title = content.split("|")[0]
    content.replace(f'{title} ', "")
    content = Content(content.split("|", pastIndex=1), removeCmd=False)
    for op, param in content.opsWithParams({"author": (slice(0,None,None), " ")}):
        with switch(op) as case:
            if case("-color"): color = param
            elif case("-image"): image = param
            elif case("-thumbnail"): thumbnail = param
            elif case("-author"):
                author = Content(" ".join(param), removeCmd=False)
                list(author.opsWithParams())
                author = str(author)
    content.formatMessage(msg, {"{title}": title, "{color}": color, "{author}": author})
    embed = discord.Embed(title=title, color=discord.Color(int(color, 16)) if color else discord.Color(0x000000))
    if image: embed.set_image(url=image)
    if thumbnail: embed.set_thumbnail(url=thumbnail)
    if author: embed.set_author(name=author)
    split = content.split("|")
    if len(split) > 1:
        for n, field in enumerate(split):
            name, value = field.split(",")
            value = Content(value, removeCmd=False)
            Inline = True if not value @ "--ninline" else False
            embed.add_field(name=name, value=str(value), inline=Inline)
    return await returnMsg(msg, embed=embed)

@command
async def emoteUsage(msg, content, cmd="emoteusage"):
    """
    gives the most used emotes
    optional params:
        emote: the emote to get the usage of
    options:
        -top <top>: gives the top <top> emotes instead of the top 10
        --least: gives the least used emotes
        --raw: gives the raw json file
        --file: gives a generated file of the most used emotes
    aliases:
        emojiusage
        emoteusage
    date: 7/10/2020
    """
    content = Content(content)
    if content @ "--raw":
        with open(emoteUsageFilePath, "rb") as f: return await returnMsg(msg, file=discord.File(f, "emoteusage.json"))
    for op, param in content.opsWithParams():
        if op == "-top":
            top = int(param)
            break
    else: top = 10
    with open(emoteUsageFilePath, "r") as j:
        data = sorted(json.load(j).items(), key=lambda x: x[1], reverse=True if not content @ "--least" else False)
        if content:
            data = {k: i for k, i in data}
            try: usage = data[str(re.findall(r'[0-9]{18}', str(content))[0])]
            except: usage = None
            return await returnMsg(msg, usage)
        else:
            emotes = []
            try:
                File = content @ "--file"
                emojiIds = [x.id for x in client.emojis]
                for n, k in enumerate(data):
                    if (n > top and not File) and len(emotes) >= top: break
                    try: emote = client.emojis[emojiIds.index(int(k[0]))]
                    except Exception as e: print(e); continue
                    emotes.append(f'<:{emote.name}:{emote.id}>: {k[1]}')
                if File: raise FileException("wanted file")
                return await returnMsg(msg, "\n".join(emotes))
            except Exception as e:
                with open("EMOTEFILE.txt", "w") as f:
                    for emote in emotes:
                        f.write(f'{emote.split(":")[1]}: {emote.split(":")[-1]}\n')
                with open("EMOTEFILE.txt", "rb") as f:
                    msg = await returnMsg(msg, file=discord.File(f, "emoteusage.txt"))
                os.remove("EMOTEFILE.txt")
                return msg

@command
async def toKelvin(msg, content, cmd="tok"):
    """
    calculates <temp> to kelvin
    example: [tok 60f
    required params:
        <temp>: the tempurature
    optional params:
        [from]: put c/f in the temp anywhere to say what unit to convert from
    added: 7/14/2020
    """
    content = Content(content)
    t = "f" if "f" in content else "c"
    content = content.string.replace(t, "").strip()
    ans = (9 / 5 * float(content) + 32) + 273 if t == "f" else float(content) + 273
    return await returnMsg(msg, str(ans))

@command
async def guessingGame(msg, content, cmd="guessinggame"):
    """
    guess a random number for 1 to [high] (defaults to 100)
    and if you guess correctly within [lives] (5 by default) tries you win
    optional params:
        high [lives]: the highest number it could be
            lives: the amount of lives, (must specify high to specify lives)
    options:
        --bet: whether or not to bet on the game
    added: 5/12/2020
    """
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

@command
async def flashEmote(msg, content, cmd="flashemote"):
    """
    makes the emote smaller then BIGGER then smaller then BIGGER
    optional params:
        emote: the emote (or technically any text) to flash
        times: the amount of times to flash
    options:
        -t <seconds>: the amount of time between each edit
    added: 7/16/2020
    """
    global Stop
    if Stop: Stop = False
    content = Content(content)
    for op, param in content.opsWithParams():
        if op in ["-time", "-t"]:
            sleepFor = float(param)
            break
    else: sleepFor = .5
    split = content.split(" ")
    emote = split[0] if split[0] else random.choice(msg.guild.emojis)
    try: times = int(split[1])
    except: times = 5
    editable = await msg.channel.send(emote)
    for x in range(times):
        if Stop:
            Stop = False
            return await returnMsg(msg, await stop("Stopped"))
        await asyncio.sleep(sleepFor)
        await editable.edit(content=f'{emote}' if editable.content == f'{emote} _ _' else f'{emote} _ _')

@command
async def bans(msg, content, cmd="bans"):
    """
    gets the bans
    """
    if not testInContent(content, "--raw"):
        with open(bannedFilePath, "r+") as bannedJ:
            data = json.load(bannedJ)
            mssg = "".join([f'{(await client.fetch_user(int(user))).name}: {" ".join(data[user])}\n' for user in data.keys()])
            try: return await returnMsg(msg, mssg)
            except: pass
    with open(bannedFilePath, "rb") as bannedJ:
        return await returnMsg(msg, file=discord.File(bannedJ, "bans.json"))

@command
async def reactionTime(msg, content, cmd="reactiontime"):
    """
    checks your reaction time
    the bot will say go, and you have to send a message
    as fast as possible
    added: 5/20/2020
    """
    await msg.channel.send("i will say GO and you have to send something as fast as possible (probably prepare the message before hand)")
    await asyncio.sleep(random.uniform(1.5, 6))
    start = time.time()
    await msg.channel.send("GO")
    try: await client.wait_for("message", check=lambda message: message.author == msg.author, timeout=60.0)
    except asyncio.TimeoutError: return await returnMsg(msg, f"{msg.author} ran out of time to react")
    else:
        end = time.time()
        return await returnMsg(msg, f'your reaction time {end - start}')

@command
async def editMsg(msg, content, cmd="editmsg"):
    """
    edits a message the blue circle sent
    required params:
        <content of new message>
    options:
        -channel <channel>: the channel the message was sent in
        --nodel: doesn't delete your command message
    added: 7/23/2020
    FORMATS (msg)
    WHITESPACE FORMATS
    """
    content = Content(content)
    if not content @ "--nodel": await msg.delete()
    for op, param in content.opsWithParams():
        if op == "-channel":
            channel = discord.utils.find(lambda x: x.name == param or x.mention == param or str(x.id) == param, msg.guild.channels)
            break
    else: channel = msg.channel
    msgId = content.split(" ")[0]
    repWith = Content(" ".join(content.split(" ")[1:]).strip(), removeCmd=False)
    msg = await channel.fetch_message(int(msgId))
    repWith.formatMessage(msg, {"{msg}": msg.content})
    repWith = repWith.whitespaceFormat(str(repWith))
    await msg.edit(content=repWith)

@command
async def isCountingMessedUp(msg, content, cmd="isCountingMessedUp"):
    """
    checks if #counting is messed up
    aliases:
        icmu
        iscountingmessedup
    added: 7/24/2020
    """
    global Stop
    channel = await client.fetch_channel(468874244021813258)
    last = math.nan
    if Stop: Stop = False
    async with msg.channel.typing():
        async for mssg in channel.history(limit=100000):
            if Stop:
                Stop = False
                return await returnMsg(msg, await stop("stopped"))
            c = mssg.content
            if c and c[-1] == ".":
                try: num = int(c.strip().replace("*", "").replace("_", "").replace("`", "").strip("."))
                except: continue
                if num > last + 1:
                    await msg.channel.send(f'{msg.author.mention} {num} is messed up')
                last = num
            else: last -= 1
    return await returnMsg(msg, "done")

@command
async def getWeather(msg, content, cmd="weather"):
    """
    gets the weather in <location>
    required params:
        <location>
    added: 7/24/2020
    """
    content = Content(content)
    if not content:
        return await returnMsg(msg, "But like where?")
    request = requests.get(f"https://www.google.com/search?q={content}+weather")
    try:
        soup = bs.BeautifulSoup(request.text, features="html.parser")
        tempurature = soup.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})[1].text
        temp = int(tempurature.split("°")[0])
        condition = soup.find_all("div", {"class": "BNeawe tAd8D AP7Wnd"})[0].text
        condition = condition.split("AM" if "AM" in condition else "PM")[1]
        location = soup.find_all("span", {"class": "BNeawe tAd8D AP7Wnd"})[0].text
        celcius = f'{5 / 9 * (float(tempurature.split("°")[0]) - 32)}°C'
    except:
        return await returnMsg(msg, "failed")
    if "Pleasanton, CA" in location: return await returnMsg(msg, "failed")
    r = int(255 * ((temp) / 134))
    b = int(0 + (1 - (temp / 134)) * 255)
    embed = discord.Embed(title=location, color=discord.Color.from_rgb(r, 0, b))
    embed.add_field(name="Current weather (F)", value=tempurature)
    embed.add_field(name="Current weather (C)", value=celcius)
    embed.add_field(name="Overhead", value=condition, inline=False)
    return await returnMsg(msg, embed=embed)

@command
async def getBaseballScore(msg, content, cmd="baseballscore"):
    """
    gets the current score for <team>'s game
    if they are not in a game, it will say when they next play
    required params:
        <team>
    options:
        --totalcolor: changes the way it calculates the color
            by default it's more red if the away team is dominating
            and more blue if the home team is dominating
            this makes it so it's the sum of the score / the highest
            scoring game in baseball
    aliases:
        baseball
        baseballscore
        mlb
    """
    content = Content(content).calcOps()
    if not content: return await returnMsg(msg, "smh man what team")
    request = requests.get(f"https://www.google.com/search?q={content}+game")
    soup = bs.BeautifulSoup(request.text, features="html.parser")
    span = soup.find_all("span", {"class": "rQMQod AWuZUe"})
    inning = span[0].text if span else "NONE"
    if inning != "NONE":
        teams = soup.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})[1:3]
        scores = soup.find_all("div", {"class": "BNeawe deIvCb AP7Wnd"})[1:3]
        t1 = (teams[0].text, int(scores[0].text))
        t2 = (teams[1].text, int(scores[1].text))
        color = (int(255 * (t1[1] / (t2[1] + t1[1]))), 0, int(255 * (t2[1] / (t2[1] + t1[1])))) if (t1[1] != 0 and t2[1] != 0) and not content @ "--totalcolor" else (int(255 * ((t1[1] + t2[1]) / 46)), 0, int(255 * (1 - ((t1[1] + t2[1]) / 46))))
        embed = discord.Embed(title=f'{t1[0]} @ {t2[0]}', color=discord.Color.from_rgb(*color))
        embed.add_field(name="Inning", value=inning)
        embed.add_field(name="Score", value=f'{t1[1]} TO {t2[1]}')
    else:
        try:
            time = soup.find_all("span", {"class": "r0bn4c rQMQod"})[0:2]
            time = f'{time[0].text}, {time[1].text}'
            teams = soup.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})[1:3]
            t1 = teams[0].text
            t2 = teams[1].text
            if "yesterday" in time.lower():
                raise Exception("Yesterday's game")
            embed = discord.Embed(title=f'{t1} @ {t2} {time} (PACIFIC TIME)')
        except Exception as e:
            winner = soup.find_all("span", {"class": "FCUp0c rQMQod"})[0]
            loser = soup.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})[2]
            scores = soup.find_all("div", {"class": "BNeawe deIvCb AP7Wnd"})[1:3]
            t1 = (winner.text, int(scores[0].text))
            t2 = (loser.text, int(scores[1].text))
            color = (int(255 * (t1[1] / (t2[1] + t1[1]))), 0, int(255 * (t2[1] / (t2[1] + t1[1])))) if (t1[1] != 0 and t2[1] != 0) or not content @ "--totalcolor" else (int(255 * ((t1[1] + t2[1]) / 46)), 0, 0)
            embed = discord.Embed(title=f'{t1[0]} WON against {t2[0]}', color=discord.Color.from_rgb(*color))
            embed.add_field(name=f"{t1[0]}'s score", value=str(t1[1]))
            embed.add_field(name=f"{t2[0]}'s score", value=str(t2[1]))

    return await returnMsg(msg, embed=embed)

@command
async def covid(msg, content, cmd="covid"):
    """
    Gets the total cases, total deaths, and total recoveries
    of the COVID-19 pandemic
    """
    request = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = bs.BeautifulSoup(request, features="html.parser")
    div = soup.find("div", {"class": "content-inner"})
    totalCases, totalDeaths, totalRecovered = map(lambda x: x.text.strip(), div.find_all("div", {"class": "maincounter-number"}))
    embed = discord.Embed(title="Covid stats", color=discord.Color(0xff0000))
    embed.add_field(name="Total Cases", value=totalCases)
    embed.add_field(name="Total Deaths", value=totalDeaths)
    embed.add_field(name="Total Recovered", value=totalRecovered)
    return await returnMsg(msg, embed=embed)