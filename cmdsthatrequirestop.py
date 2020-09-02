from common import *

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

@command
async def flashEmote(msg, content, cmd="flashemote"):
    """
    makes the emote smaller then BIGGER then smaller then BIGGER
    optional params:
        emote: the emote (or technically any text) to flash
        times: the amount of times to flash
    options:
        -t <seconds>: the amount of time between each edit
    CATEGORY: FUN
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
async def spamCmd(msg, content, cmd="spam"):
    """
    spams <message> over and over again :)
    required params:
        <amount>: the amount of times to spam
        <message>: the message to spam
        OR
        -random *<op> (sep with |): picks randomly from the ops seperated by |
    FORMATS AND {count}, {rcount}, {lauthor}
    aliases:
        spam
        spamcmd
    CATEGORY: FUN
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

    if messages < 0: return await returnMsg(msg, "message count can't be less than 0")

    if "-random" in c:
        c.replace("-random ", "")
        c = " ".join(c.split(" ")[1:])
        options = c.split("|")
        return await spam(msg, int(messages), options)

    message = " ".join(c.split(" ")[1:])
    await spam(msg, messages, [message])
    if random.random() >= .99: await msg.channel.send("You found an easter egg hehe")
    else: return await returnMsg(msg, random.choice(("done", "Done")))

@command
async def response(msg, content, cmd="response"):
    """
    finds the message after <message> in chat with a limit that defaults to 1000
    required params:
        <message>: the message to search for
    options:
        -lim <limit>: the limit of messages to search
    CATEGORY: misc
    added: 5/20/2020
    """
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


async def _deathBattle(msg, users, going, notGoing, responseTime, damageMsgs, healMsgs, embed, first, second, editable):
    global playingDB, Stop
    if Stop:
        Stop = False
        await removeFromList(playingDB, going, notGoing)
    tempItems = {}
    for item in users[going]["items"]:
        t = findItem(iName=item)
        tempItems[t["id"]] = t["name"].lower()
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
            t = findItem(iId=int(i))
            await RAMUserInfo[going.id].removeItem(item=t)
            AH = t["name"]
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
                        AH = random.choice(list(users[notGoing]["items"].keys()))
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
                    health = float(health.content)
                except:
                    await msg.channel.send("you waited too long, picking 15")
                    health = 15
                if health > 200:
                    await msg.channel.send("too high, you get to do NOTHING")
                    if going == first:
                        await _deathBattle(msg, users, second, first, responseTime, damageMsgs, healMsgs, embed, first, second, editable)
                    else: await _deathBattle(msg, users, first, second, responseTime, damageMsgs, healMsgs, embed, first, second, editable)
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
        await RAMUserInfo[int(going.id)].addMoney(-20)
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
        await RAMUserInfo[int(first.id)].addMoney(abs(users[second]["health"]))
        await RAMUserInfo[int(second.id)].addMoney(users[second]["health"])
        return await msg.channel.send(f'{first.name} has won!\nthey earned {abs(users[second]["health"])} and {second.name} has lost {abs(users[second]["health"])}')
    elif users[first]["health"] <= 0:
        await removeFromList(playingDB, going, notGoing)
        await RAMUserInfo[int(second.id)].addMoney(abs(users[second]["health"]))
        await RAMUserInfo[int(first.id)].addMoney(users[second]["health"])
        return await msg.channel.send(f'{second.name} has won!\nthey earned {abs(users[first]["health"])} and {first.name} has lost {abs(users[first]["health"])}')
    else:
        if going == first:
            await _deathBattle(msg, users, second, first, responseTime, damageMsgs, healMsgs, embed, first, second, editable)
        else: await _deathBattle(msg, users, first, second, responseTime, damageMsgs, healMsgs, embed, first, second, editable)

@command
async def deathbattle(msg, content, cmd="deathbatte"):
    """
    battle a user ``````diff
-TO THE DEATH!!!!!!! DA DA DAAAAAAAAAAAAAAAAAAAAAA``````
    required params:
        <user>: the user to ***FIGHT***
    aliases:
        db
        deathbattle
    CATEGORY: games&money
    added: 6/11/2020
    """
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
    await UserInfo.registerUser(user2.id)
    b1 = RAMUserInfo[msg.author.id].level // 3
    b2 = RAMUserInfo[user2.id].level // 3
    first = random.choice([msg.author, user2])
    second = msg.author if first == user2 else user2
    playingDB.append(first)
    playingDB.append(second)
    i1 = RAMUserInfo[msg.author.id].items
    i2 = RAMUserInfo[user2.id].items
    users = {msg.author: {"user": msg.author, "health": 100 + b1, "items": i1, "healstreak": 0},
             user2: {"user": user2, "health": 100 + b2, "items": i2, "healstreak": 0}}
    users[second]["health"] += 15
    embed.add_field(name="MOVE", value="START", inline=False)
    for user in users.values():
        embed.add_field(name=user["user"].name, value=user["health"])
    damageMsgs = ["{attaker} punched {aked} for {damage}", "{attaker} fireballed {aked} for {damage}", "{attaker} summoned a meteor and it hit {aked} for {damage}", "{aked} was unconsious and a pickle came FLYING at {aked} they took {damage} damage"]
    healMsgs = ["{attaker} was healed for {damage}", "{attaker} was blessed with {damage} extra health"]
    editable = await msg.channel.send(embed=embed)
    await _deathBattle(msg, users, first, second, responseTime, damageMsgs, healMsgs, embed, first, second, editable)

@command
async def isCountingMessedUp(msg, content, cmd="isCountingMessedUp"):
    """
    checks if #counting is messed up
    aliases:
        icmu
        iscountingmessedup
    CATEGORY: info
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
async def stopCmd(msg, content, cmd="stop"):
    """
    stops something spammy
    aliases:
        stop
        stopcmd
    CATEGORY: misc
    """
    global Stop
    Stop = await stop(retstop=True)
    return await returnMsg(msg, "stopped")