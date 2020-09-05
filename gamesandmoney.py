from common import *

command.setCategory("games&money", "games")

@command
async def guessingGame(msg, content, cmd="guessinggame"):
    """
    guess a random number for 1 to [high] (defaults to 100)
    and if you guess correctly within [lives] (5 by default) tries you win
    money is calculated as so
        floor(answer / startinglives)
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
        except: return await returnMsg(msg, "waited too long")
        if c in ["stop", "giveup", "cancel"]:
            return await returnMsg(msg, embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(100, 0, 0)))
        LIVES -= 1
        if int(c) == ans:
            say = f"YOU WIN\nWITH {LIVES} LIVES LEFT" if not Bet else f'YOU WIN\nWITH {LIVES} LIVES LEFT\nYou earned {(int(ans) // STARTLIVES)}'
            if Bet: await RAMUserInfo[msg.author.id].addMoney(int(ans) // STARTLIVES)
            return await returnMsg(msg, embed=discord.Embed(title=say, color=discord.Color.from_rgb(0, 255, 0)))
        elif LIVES <= 0:
            say = f"YOU LOSE\nTHE ANSWER WAS {ans}" if not Bet else f'YOU LOSE\nTHE ANSWER WAS {ans}\nYOU LOSE {(int(ans) // STARTLIVES)}'
            if Bet: await RAMUserInfo[msg.author.id].addMoney(-(int(ans) // STARTLIVES))
            return await returnMsg(msg, embed=discord.Embed(title=say, color=discord.Color.from_rgb(255, 0, 0)))
        await msg.channel.send(f"{msg.author.mention} too high\nguess\nyou have {LIVES} lives left" if int(c) > ans else f"{msg.author.mention} too low\nguess\nyou have {LIVES} lives left")

@command
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
    resp1=resp2 = "??????"
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
        await UserInfo.registerUser(user2.id)
        if opps[resp2] == resp1:
            if user2.mention != user1.mention:
                await RAMUserInfo[user2.id].addMoney(random.randint(1, 5))
                await RAMUserInfo[user1.id].addMoney(random.randint(-5, -1))
            return await returnMsg(msg, f'{user2.mention} WINS')
        elif opps[resp1] == resp2:
            if user2.mention != user1.mention:
                await RAMUserInfo[user2.id].addMoney(random.randint(-5, -1))
                await RAMUserInfo[user1.id].addMoney(random.randint(1, 5))
            return await returnMsg(msg, f'{user1.mention} WINS')
        else: await msg.channel.send("ITS A DRAW")
    else: await msg.channel.send("either someone spelled something wrong, or someone isn't playing by the rules")

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
async def hangman(msg, content, cmd="hangman"):
    """
    ping a user and play hangman, you have 15 seconds to dm the bot a word and the user will have ot guess it
    required params:
        <user>: the user to play
    added: 6/1/2020
    """
    content = Content(content)
    user = content.getUser(msg, 0)
    if user.id in playingHangman.keys():
        return await returnMsg(msg, f'{msg.author.mention} {user.name} is already in a game')
    try: lives = int(content.split(" ")[1])
    except: lives = 9
    playingHangman[user.id] = None
    await msg.author.send(f"you will have 15 seconds to send a word of your choice, and {user.name} will have to guess it in {msg.channel.name}")
    await asyncio.sleep(15)
    word = None
    async for i in msg.author.dm_channel.history(limit=1):
        word = i.content
    disp = "".join(["-" if x not in (" ", "," "." "'" '"') else x for x in word])
    playingHangman[user.id] = {"word": word, "lives": lives, "guessed": [], "disp": disp}
    await msg.channel.send(f'{user.mention} guessing time')
    mssg = await msg.channel.send(disp)
    try: await client.wait_for("message", check=lambda message: message.author.id == user.id, timeout=90.0)
    except: return await returnMsg(msg, "user did not respond in 1.5 minutes")

@command
async def mmoney(msg, content, cmd="mmoney"):
    """
    your *money*
    optional params:
        [user]: the user's *money*
    options:
        --raw: the raw file of *money*
        --totalmoney: gets the total money, and [users] (default to your) % of the money
    aliases:
        mmoney
        bal
        mymoney
        money
    added: 5/10/2020
    History:
        this used to be a joke command <:TiredPuffle:707773683854213140>
    """
    user = Content(content.split(" --totalmoney")[0]).getUser(msg, 0)
    await UserInfo.registerUser(user.id)
    if random.random() >= .99:
        loss = round(random.random(), 2)
        RAMUserInfo[msg.author.id].money -= loss
        s = random.choice((
            f"while opening your wallet someone somehow stole some money you lost {loss}",
            f'while opening your wallet you spilled some coins and lost {loss}'
        ))
        await msg.channel.send(s)
    if "--totalmoney" in content:
        total = 0
        for u in RAMUserInfo.values():
            await u.dumpMoneyInfo()
        with open(moneyDataFilePath, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            for amnt in data.values():
                total += amnt
        return await returnMsg(msg, f'total money: {total}\n{user.name}\'s % of the total: {RAMUserInfo[user.id].money / total * 100}')
    if "--raw" in content:
        with open(moneyDataFilePath, "rb", encoding="utf-8-sig") as f:
            return await returnMsg(msg, file=discord.File(f, "money.json"))
    return await returnMsg(msg, f'{user.name} has €{RAMUserInfo[user.id].money}')

@command
async def shop(msg, content, cmd="shop"):
    """
    lists all items available for purchace in the shop
    added: 6/11/2020
    """
    with open(itemsFilePath, "r") as j:
        data = json.load(j)
        embed = discord.Embed(title="Items", color=discord.Color(0x00ff00))
        for item in data:
            embed.add_field(name=f'{item["id"]}: {item["name"]}', value=f'Description: {item["desc"]}\nCost: €{item["cost"]}')
        return await returnMsg(msg, embed=embed)

@command
async def inventory(msg, content, cmd="inv"):
    """
    lists the items in your inventory
    optional params:
        [user]: the user's inventory you want to see
    aliases:
        inventory
        items
        inv
    added: 6/11/2020
    """
    content = Content(content)
    user = content.getUser(msg)
    userInfo: UserInfo = RAMUserInfo[msg.author.id]
    await userInfo.dumpItemInfo()
    items = userInfo.items
    if items:
        embed = discord.Embed(name=f"{user.name}'s inventory", color=user.color)
        for item, count in items.items():
            embed.add_field(name=item, value=count)
        return await returnMsg(msg, embed=embed)
    else: return await returnMsg(msg, "none")

@command
async def buyItem(msg, content, cmd="buyitem"):
    """
    buys an item from the shop
    aliases:
        buyitem
        buy
    added: 6/11/2020
    """
    buying = Content(content).string
    if ", " in content:
        amnt = int(buying.split(", ")[1])
        buying = buying.split(", ")[0]
    else: amnt = 1
    money = RAMUserInfo[msg.author.id].money
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
    l = RAMUserInfo[msg.author.id].items
    try: l[forPurchase["name"]] += amountBought
    except: l[forPurchase["name"]] = amountBought
    RAMUserInfo[msg.author.id].money = money
    return await returnMsg(msg, f'bought {forPurchase["name"]}')

@command
async def mostmoney(msg, content, cmd="mostmoney"):
    """
    a leaderboard of the people with the most money
    i finally gave in lol
    options:
        -top <top>: the amnt of people to show
        -sep <seperator>: what to seperate each person by
    aliases:
        tmoney
        mostmoney
        lbm
        lbmoney
        topm
        top m
        top --money
        top --m
        top --bal
    added: 8/19/2020
    """
    content = Content(content)
    top = 5
    sep = ""
    for op, param in content.opsWithParams():
        if op == "-top": top = param
        elif op == "-sep": sep = Content.whitespaceFormat(param)
    for u in RAMUserInfo.values():
        await u.dumpMoneyInfo()    
    with open(moneyDataFilePath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        data = {uId: amnt for uId, amnt in sorted(data.items(), key=lambda x: x[1], reverse=True)}
        new = []
        USERS = {u.id: u.name for u in msg.guild.members}
        total = 0
        for n, (uId, amnt) in enumerate(data.items()):
            try: 
                if n < int(top):
                    USERS[int(uId)]
                    new.append(f'```{n + 1}: {USERS[int(uId)]}: {amnt}')
                total += amnt
            except KeyError: continue
        for n, (_, amnt) in zip(new, data.items()):
            new[new.index(n)] += f"         % of total: {amnt / total * 100}```"
        return await returnMsg(msg, f'total money: {total}\n{sep.join(new)}')

@command
async def slotmachine(msg, content, cmd="slotmachine"):
    """
    CUSTOM:
```gambling time``````rules:
    jackpot = 50-100
    win = gauss, mean=4, stdev=2
    bar + 7 = gauss, mean=0, stdev=1
    7 = win + 1 * amnt of 7s
    bar = lose - 1 * amnt of bars
    lose = 0-(-15)
    odds of jackpot 1/210``````aliases:
    slots
    slotmachine
    gamble
    WIN
    LOSE``````added: 9/3/2020```"""
    userInfo: UserInfo = RAMUserInfo[msg.author.id]
    spaces = (
        "7", "BAR", ":peach:", 
        ":grapes:", "<:sev:627342162647842826>", ":thumbsdown:",
        ":thumbsup:", ":toilet:", "<:hashno:596148433572724749>",
        "<:troy:590386275748544523>")
    answer = tuple(random.choice(spaces) for _ in range(3))
    if answer == ("<:sev:627342162647842826>", "<:sev:627342162647842826>", "<:sev:627342162647842826>"):
        await userInfo.giveAchievement(msg, 777)
    Bar = "BAR" in answer
    Seven = "7" in answer
    if Bar and Seven:
        amnt = round(random.gauss(0, 1))
        send = f"you had bar and 7 you {'lose'*(amnt < 0)+'win'*(amnt >= 0)} {amnt}"
        color = 0xbbbbbb
    elif Bar:
        amnt = random.randint(-15, 1) - (1 * (4 - len(set(answer))))
        print(1 * (4 - len(set(answer))))
        send = f"BAR:\nAUTO LOSS\nYou lose {amnt}"
        color = 0xff0000
    elif len(set(answer)) == 1:
        amnt = random.randint(50, 100)
        send = f"YOU WIN THE JACKPOT\nYOU WON {amnt}"
        color = 0x00ff00
    elif Seven:
        amnt = round(random.gauss(4, 2)) + (1 * (4 - len(set(answer))))
        print(1 * (4 - len(set(answer))))
        send = f"7:\nAUTO WIN\nYou win {amnt}"
        color = 0x00ffff
    elif len(set(answer)) == 2:
        amnt = round(random.gauss(4, 2))
        if amnt < 0:
            send = f'You got 2 of the same\nHowever you were unlucky and lost money anyway'
        else:
            send = f'You got 2 of the same\nYOU WON {amnt}'
        color = 0x00ffff
    else:
        amnt = random.randint(-15, 1)
        send = f"better luck next time\nyou lost {amnt}"
        color = 0xff0000
    await userInfo.addMoney(amnt)
    embed = discord.Embed(title=f'{msg.author.name}\n{send}', color=color)
    embed.add_field(name="result", value=f'[{answer[0]} {answer[1]} {answer[2]}]')
    return await returnMsg(msg, embed=embed)