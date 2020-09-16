from os import remove
from re import sub

from requests import exceptions
from customcmds import removeCustomCmd
from common import *

command.setCategory("FUN", "fun commands")

@command
async def luckynumber(msg, content, cmd="luckynumber"):
    """
    gives author's luckynumbers
    optional params:
        [user/message]: user/messages's lucky numbers
    options:
        -c <amount>: the amount of lucky numbers
    added: 6/19/2020
    """
    content = Content(content)
    who = msg.author.mention
    count = 3
    for op, param in content.opsWithParams():
        if op == "-c":
            try: count = int(param)
            except: return await returnMsg(msg, "amount of numbers must be an integer")
    if content: who = content
    nums = " ".join([str(random.randint(1, 10)) for _ in range(count)])
    if random.random() >= .999: return await returnMsg(msg, f"{who}'s lucky numbers are 7 7 7")
    return await returnMsg(msg, f"{who}'s lucky numbers are {nums}")

@command
async def shrug(msg, content, cmd="shrug"):
    """
    shrugs
    options:
        -t <time>: the time between edits
            defaults to .3
    added: 5/23/2020
    """
    msg = await msg.channel.send(content=r"¯\_(ツ)_/¯")
    content = Content(content)
    sleepTime = .3
    for op, param in content.opsWithParams():
        if op == "-t":
            sleepTime = float(param)
    for state in ("¯\\\-(ツ)-/¯", "¯\_(ツ)_/¯"):
        await asyncio.sleep(.3)
        await msg.edit(content=state) 
    return msg

@command
async def editCmd(msg, content, cmd="edit"):
    """
    sends a message, then edits it
    ex:
        [edit cool| %o>>e
    required params:
        *<message> (sep with |): the first message will send immediately
            messages after | will be edited in, in intervals
            operators (do these instead of a message):
                +: add, defaults to add
                    tacks on the next message to the end of the last
                -: removes the message from the previous
                *: duplicates the message
                <<: adds to the beginning
                %v>>v2: replaces v with v2, do MSG for the whole message
                ^pos<<val: inserts val at pos
                ^pos=val: sets pos to val
                ;: starts a new message put --d to delete the old one
    options:
        -t <time>: the time to wait before editing each message
        -sep <sep>: defaults to nothing, replaces | with sep
        per edit: /-t <time>: the time to wait for that edit
    FORMATS
    WHITESPACE FORMATS
    aliases:
        edit
        editcmd
    added: 6/30/2020
    """
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
    tokens = enum(
        add = "+",
        min = "-",
        mul = "*",
        insertBeginning = "<",
        replace = "%",
        insert = "^",
        newMsg = ";"
    )
    while edits:
        edits.pop(0)
        if not edits: break
        token = edits[0][0]
        ChangeT = "/-t" in edits[0]
        if ChangeT:
            tempSleepFor = sleepFor
            t = edits[0]
            sleepFor = float(t.split("/-t")[1].strip())
            edits[0] = edits[0].split("/-t")[0]
        await asyncio.sleep(sleepFor)
        if not tokens.getByValue(token) or token == tokens.add: await editable.edit(content=editable.content + f'{sep}{edits[0]}')
        elif token == tokens.mul: await editable.edit(content=editable.content*int(edits[0][1:]))
        elif token == tokens.replace:
            rep = edits[0].split("%")[1].split(">>")[0]
            repWith = edits[0].split(">>")[1]
            await editable.edit(content=editable.content.replace(rep if rep != "MSG" else editable.content, repWith))
        elif token == tokens.insert:
            pos = edits[0].split("^")[1]
            splitW = "<<" if "<<" in pos else "="
            pos = pos.split(splitW)[0]
            repWith = edits[0].split(splitW)[1]
            foo = Content(editable.content, removeCmd=False)
            if splitW == "<<":
                foo.insert(int(pos), repWith)
            else: foo[int(pos)] = repWith
            await editable.edit(content="".join(foo))
        elif token == tokens.insertBeginning and edits[0][1] == "<":
            await editable.edit(content=f'{edits[0][2:]}' + editable.content)
        elif token == tokens.newMsg:
            send = Content(edits[0].split(";")[1], removeCmd=False)
            if send @ "--d":
                await editable.delete()
            editable = await editable.channel.send(send)

        else: await editable.edit(content=editable.content.replace(edits[0][1:], ""))
        if ChangeT: sleepFor = tempSleepFor

@command
async def duplicator(msg, content, cmd="duplicator"):
    """
    duplicates a message 2 times by default
    required params:
        <message>: the message to duplicate
    optional params:
        [times]: if specifying times, put it before the message
    options:
        -sep <seporator>: the string to seperate each duplicate by
            defaults to space
            WHITESPACE FORMATS
    aliases:
        duplicate
        duplicator
    added: 6/13/2020
    """
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

@command
async def ship(msg, content, cmd="ship"):
    """
    makes a cute couple out of 2 messages :)))))
    required params:
        <1>, <2>: the 2 things to be shipped seperated by comma and space
    aliases:
        ship
        boat
        SECRET:
        boip
    """
    one, *two = Content(content).split(", ")
    two = ", ".join(two)
    shipped = one[:(len(one) // 2) + 1] + two[len(two) // 2:]
    return await returnMsg(msg, "DISCLAIMER: I DO NOT SUPPORT SHIPPING PEOPLE IN ANY WAY, HOWEVER MY MASTER SEEMS TO HAVE OTHER PLANS" if random.random() >= .985 else shipped)

@command
async def echo(msg, content, cmd="echo"):
    """
    says <message> it and deletes your message
    required params:
        <message>: the message it says
    options:
        -e: makes an embed [color (rand)]: gives the embed a color, rand makes it random color
        -wait <time>: waits time before sedning, still deletes your message instantly
        -fops *<key="val"> (sep with ,): every {key} in your message will be replaced with val, val must be in ""
        -formatops: alias to -fops
        --dm: dms you
        --nodel: doesn't delete your message
        --tts: uses text to speach
    aliases:
        echo
        e
 
    added: 12/14/19
    """
    c = Content(content)
    defaultOps = {"{echo}": str(c).replace("{echo}", "")}
    formatOps = {}
    if not c @ "--nodel":
        try: await msg.delete()
        except: pass
    for op, param in c.opsWithParams():
        if op == "-e":
            if param: 
                color = int(param, 16) if param != "rand" else random.randint(0, 16777215)
            else: color = 0x000000
            embed = discord.Embed(title=str(c), color=discord.Color(color))
            return await returnMsg(msg, None, embed=embed) if not c @ "--dm" else await msg.author.send(embed=embed)
        elif op == "-wait":
            try: await asyncio.sleep(float(param))
            except: return await returnMsg(msg, "-wait must be float")
        elif op in ("-formatops", "-fops"):
            if not Content(str(param), removeCmd=False).suitibleForEval():
                return await returnMsg(msg, "nice try")
            formatOps = eval(f'dict({param})')
            formatOps = {k: v for k, v in map(lambda x: ("{" + x[0] + "}", x[1]), formatOps.items())}
    ops = {**defaultOps, **formatOps}
    c.formatMessage(msg, ops)
    return await returnMsg(msg, str(c), tts=c @ "--tts") if not c @ "--dm" else await msg.author.send(str(c), tts=c @ "--tts")
@command
async def embed(msg, content, cmd="embed"):
    """
    creates an embed
    required params:
        <title> | *<fields <title>, <value> (--ninline)> 
        seperate each field with |
        example:
        [embed Title | Field1, Field content1 | Field2, Field content2
    options:
        -color <color> (rand): the color of the embed
            rand: makes a random color
        -image <img url>: the image of the embed
        -author <author>: the author of the embed
    FORMATS (title, color, author)
    added: 7/10/2020
    """
    content = Content(content)
    color=image=thumbnail=author=msgContent = None
    for op, param in content.opsWithParams():
        with switch(op) as case:
            if case("-color"): color = param
            elif case("-image"): image = param
            elif case("-thumbnail"): thumbnail = param
            elif case("-author"):
                author = Content(param, removeCmd=False)
                list(author.opsWithParams())
                author = str(author)
            elif case("-content"):
                msgContent = param
    title = content.split("|")[0]
    title = str(Content(title, removeCmd=False).formatMessage(msg, {"{title}": title, "{color}": color, "{author}": author}, ret=True))
    content.formatMessage(msg, {"{title}": title, "{color}": color, "{author}": author})
    embed = discord.Embed(title=title, color=discord.Color(int(str(color), 16) if color != "rand" else random.randint(0, 16777215)) if color else discord.Color(0x000000))
    if image: embed.set_image(url=image)
    if thumbnail: embed.set_thumbnail(url=thumbnail)
    if author: embed.set_author(name=author)
    split = content.split("|")[1:]
    if len(split) >= 1 and split[0] and (len(split) >=1 and split[0].strip() != title.strip()):
        for n, field in enumerate(split):
            name, value = field.split(",")
            value = Content(value, removeCmd=False)
            Inline = not (value @ "--ninline")
            embed.add_field(name=name, value=str(value), inline=Inline)
    return await returnMsg(msg, content=msgContent, embed=embed)

@command
async def magicBall(msg, content, cmd="8ball"):
    """
    the mAgiC 8ball ooooooooooooooo spoooooky
    optional params:
        [question]: ask it a question :)
    options:
        -e [color]: makes the answer an embed
            [color] specifies the color defaults to black
    FORMATS (question)
    WHITESPACEFORMATS
    aliases:
        magicball
        8
        8ball
        7ball
    added: 11/6/19
    """
    with open(mballresponseFilePath, "r") as f:
        responses = f.read().split("\n")
    choice = Content(random.choice(responses), removeCmd=False)
    choice.formatMessage(msg, {"{question}": cutCmd(content)})
    choice._whitespaceFormat()
    for op, param in Content(content).opsWithParams():
        if op == "-e":
            return await returnMsg(msg, embed=discord.Embed(title=choice, color=int(param, 16) if param else 0x000000))
    return await returnMsg(msg, choice)

@command
async def randomFace(msg, content, cmd="randomface"):
    """
    generates a random face
    aliases:
        rface
        randface
    """
    BROWS, EYES, MOUTHS = ((">", "|"), (":", ";"), (")", "(", "{", "}", "[", "]", "p", "P", "d", "l", "C", "c"))
    if random.random() >= .995:
        return await returnMsg(msg, "()-()\n ___")
    if random.random() >= .8:
        return await returnMsg(msg, f'{random.choice(BROWS)}{random.choice(EYES)}{random.choice(MOUTHS)}')
    else:
        return await returnMsg(msg, f'{random.choice(EYES)}{random.choice(MOUTHS)}')

@command
async def twc(msg, content, cmd="twc"):
    """
    the wave command
    aliases:
        thewavecommand
        twc
        tpc
        thepenguincommand
    """
    return await returnMsg(msg, random.choice(("very nice!", "very cool!", "<:TiredPuffle:707773683854213140>")))

@command
async def unicodeChar(msg, content, cmd="unicodechar"):
    """
    generates a random unicode character
    optional params:
        [amount]: the amount of characters to generate
    options:
        -sep <seperator> (WHITESPACEFORMATS): seperates each character by seperator
        -bynum *<nums>: gets a unicode character by number
    aliases:
        ucodechar
        unicodechar
    added: 11/9/19
    """
    content = Content(content)
    sep = "\n"
    send = []
    for op, param in content.opsWithParams():
        if op == "-sep":
            sep = Content.whitespaceFormat(param)
        elif op == "-bynum":
            for num in param.split(" "):
                send.append(chr(int(num)))
    try: amount = int(content)
    except: amount = 1
    if "-bynum" not in content.opOps: send = [chr(random.randint(0, 185000)) for _ in range(amount)]
    return await returnMsg(msg, sep.join(send))

@command
async def spacer(msg, content, cmd="spacer"):
    """
    spaces the <message> you give it by <amount>
    required params:
        [amnt] <message>: the message to space
            amnt is the amount of spaces
    options:
        -sep <seperator> (WHITESPACEFORMATS): instead of a space it seperates by seperator
        --nodel: doesn't delete your message
    """
    sep = " "
    content = Content(content)
    if not content @ "--nodel":
        try: await msg.delete()
        except: pass
    try: 
        spaces, *c = content.split(" ")
        spaces = int(spaces)
        c = " ".join(c)
    except: 
        c = content
        spaces = 1
    if "-sep" in c:
        sep = content.split("-sep ")[1]
        c = c.split("-sep")[0]
        sep = Content.whitespaceFormat(sep)
    add = sep * int(spaces)
    word = add.join(c)
    return await returnMsg(msg, word)

@command
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

@command
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
            if (mssg[val - 1] != " " and newPhrase[val - 1].islower()) \
            or (newPhrase[val - 2].islower() and mssg[val - 1] == " "):
                letter = letter.upper()
        newPhrase.append(letter)

    return await returnMsg(msg, "".join(newPhrase))

@command
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

@command
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

@command
async def reverse(msg, content, cmd="reverse"):
    """
    reverses your message
    requried params:
        <message>
    aliases:
        reversed
        SECRET:
        esrever
        desrever
    """
    return await returnMsg(msg, cutCmd(content)[::-1])

@command
async def pigLatin(msg, content, cmd="piglatin"):
    """
    onvertscay essagemay intoay igpay atinlay
    equiredray aramspay:
        <message>: ethay essagemay otay onvertcay otay igpay atinlay
        --kc: eepskay asingcay
    addeday: 5/10/2020
    aliases:
        piglatin
        pl
        SECRET:
        igpayatinlay
    """
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

@command
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
            150 < iq < 200: f"that's a pretty high iq: {iq}",
            50 < iq <= 150: iq,
            0 <= iq <= 50: f"you good there mate, your iq is {iq}",
            iq < 0: f"you literally don't have a brain you somehow have a negative iq idek\nIQ: {iq}"}.get(True))

@command
async def sports(msg, content, cmd="sports"):
    """
    gets the current score for <team>'s game (google should be able to figure out what sport you're talking)
    if they are not in a game, it will say when they next play
    required params:
        <team>
    aliases:
        baseball
        baseballscore
        mlb
        sports
        nfl
        genflscore
        nflscore
        nflgame
        footballscore
        football
        AmErIcAnFoOtBaLl
        nba
        nbascore
        nhlscore
        nhl
        mls
        mlsscore
    """
    content = Content(content).calcOps()
    if not content: return await returnMsg(msg, "smh man what team")
    request = requests.get(f"https://www.google.com/search?q={content}+game")
    soup = bs.BeautifulSoup(request.text, features="html.parser")
    span = soup.find_all("span", {"class": "rQMQod AWuZUe"})
    inning = span[0].text if span else "NONE"
    retContent = None
    if inning != "NONE": #if the game is on
        teams = soup.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})[1:3]
        scores = soup.find_all("div", {"class": "BNeawe deIvCb AP7Wnd"})[1:3]
        t1 = (teams[0].text, int(scores[0].text))
        t2 = (teams[1].text, int(scores[1].text))
        AsWinning = False
        As = t1 if "athletics" in t1[0] else False
        if not As: t2 if "athletics" in t2[0] else False
        if As:
            if As == t2: AsWinning = As[1] > t1[1]
            else: AsWinning = As[1] > t2[1]
        color = (int(255 * (t1[1] / (t2[1] + t1[1]))), 0, int(255 * (t2[1] / (t2[1] + t1[1])))) if (t1[1] != 0 and t2[1] != 0) and not content @ "--totalcolor" else (int(255 * ((t1[1] + t2[1]) / 46)), 0, int(255 * (1 - ((t1[1] + t2[1]) / 46))))
        embed = discord.Embed(title=f'{t1[0]} @ {t2[0]}', color=discord.Color.from_rgb(*color))
        embed.add_field(name="Inning" if cmd in ("mlb", "baseball", "baseballscore") else "Time", value=inning)
        embed.add_field(name="Score", value=f'{t1[1]} TO {t2[1]}')
        if inning == 7 and int(t1[1]) == 7 and int(t2[1]) == 7:
            await RAMUserInfo[msg.author.id].giveAchievement("7-7-7")
        retContent = "GO A'S" if AsWinning else None
    else: #if the game is over or hasnt' started
        try:
            time = soup.find_all("span", {"class": "r0bn4c rQMQod"})[0:2]
            time = f'{time[0].text}, {time[1].text}'
            teams = soup.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})[1:3]
            t1 = teams[0].text
            t2 = teams[1].text
            if "yesterday" in time.lower():
                raise Exception("Yesterday's game")
            embed = discord.Embed(title=f'{t1} @ {t2} {time} (PACIFIC TIME)')
        except:
            winner = soup.find_all("span", {"class": "FCUp0c rQMQod"})[0]
            loser = soup.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})[2]
            scores = soup.find_all("div", {"class": "BNeawe deIvCb AP7Wnd"})[1:3]
            t1 = (winner.text, int(scores[0].text))
            t2 = (loser.text, int(scores[1].text))
            color = (int(255 * (t1[1] / (t2[1] + t1[1]))), 0, int(255 * (t2[1] / (t2[1] + t1[1])))) if (t1[1] != 0 and t2[1] != 0) or not content @ "--totalcolor" else (int(255 * ((t1[1] + t2[1]) / 46)), 0, 0)
            embed = discord.Embed(title=f'{t1[0]} WON against {t2[0]}', color=discord.Color.from_rgb(*color))
            embed.add_field(name=f"{t1[0]}'s score", value=str(t1[1]))
            embed.add_field(name=f"{t2[0]}'s score", value=str(t2[1]))

    return await returnMsg(msg, content=retContent, embed=embed)

@command
async def changenick(msg, content, cmd="changenick"):
    """
    changes the nick name of the bot
    required params:
        <name>: the name to change to
    options:
        --nret, makes it not say "did it work"
    aliases:
        nick
        nickname
        changenick
    added: 8/19/2020
    """
    content = Content(content)
    Ret = not (content @ "--nret")
    member = await msg.guild.fetch_member(client.user.id)
    await member.edit(nick=content.string)
    if Ret: return await returnMsg(msg, "did it work?")

@command
async def triangulate(msg, content, cmd="triangulate"):
    """
    makes text do this:
    hello
    hell
    he
    h
    required params:
        <text>
    aliases:
        triangulatetext
        triangulatetxt
        triangletext
        triangletxt
        tritext
        tritxt
        SECRET:
        triangulatetex
        triangulatete
        triangulatet
        triangulate
        triangulat
        triangula
        triangul
        triangu
        triang
        trian
        tria
        tri
        tr
        t
    added: 9/3/2020
    """
    content = cutCmd(content)
    send = []
    for i in range(len(content)):
        add = content[::-1][:i + 1][::-1].strip()
        if add not in send:
            send.append(add)
    send = send[::-1]
    return await returnMsg(msg, "\n".join(send))

@command
async def listachievements(msg, content, cmd="achievements"):
    """
    lists the achievements
    options:
        --raw: the file
    aliases:
        listachievements
        listachmnts
        lachmnts
    added: 9/3/2020
    """
    content = Content(content)
    if content @ "--raw":
        with open(achievementsJson, "rb") as f:
            return await returnMsg(msg, file=discord.File(f, "achievements.json"))
    with open(achievementsJson, "r", encoding="utf-8-sig") as j:
        data = json.load(j)
        embed = discord.Embed(title="achievements")
        for achievement in data:
            embed.add_field(name=achievement["name"], value=f"description: {achievement['desc']}\nid: {achievement['id']}")
        return await returnMsg(msg, embed=embed)

@command
async def achievements(msg, content, cmd="achievements"):
    """
    lists your achievements
    optional params:
        [user]: the user to get the achievements of
    options:
        --html: generates an html file
    aliases:
        achievements
        myachievements
        myachmnts
        machmnts
    """
    content = Content(content).calcOps()
    user = content.getUser(msg)
    userInfo: UserInfo = RAMUserInfo[user.id]
    if content @ "--html":
        with open(f'{user.id}A.html', "w") as f:
            f.write(f"""<html><head><meta charset="utf-8"><title>{user.name}</title>
<style>
    p:hover{{
        background-color:#00ff0055;
    }}
</style>
<body style="font-family:arial"><h1 style="color:green">Achievements</h1>""")
            for achievement in userInfo.achievements:
                ach = getAchievement(id_=achievement)
                f.write(f"""<p>Name: {ach["name"]}<br />Description: {ach["desc"]}</p> <hr>""")
        with open(f'{user.id}A.html', "rb") as f:
            rv = await returnMsg(msg, file=discord.File(f, "achievements.html"))
        os.remove(f'{user.id}A.html')
        return rv
    embed = discord.Embed(title="achievements")
    for achievement in userInfo.achievements:
        if not achievement: continue
        ach = getAchievement(id_=achievement)
        embed.add_field(name=ach["name"], value=f'description: {ach["desc"]}')
    return await returnMsg(msg, embed=embed)

@command
async def usermosaic(msg, content, cmd="usermosaic"):
    """
    generates an html file of all user profiles
    aliases:
        usermosaic
        avatars
    added: 7/23/2020
    """
    with open("mosaic.html", "w", encoding="utf-8") as f:
        f.write(f"""<html><head><meta charset="utf-8"></head>
<body>
    {"".join(f'<img src={user.avatar_url} title="{user.name.replace("<", "&lt;").replace(">", "&gt;")}">' for user in msg.guild.members)}
</body>""")
    with open("mosaic.html", "rb") as f:
        rv = await returnMsg(msg, file=discord.File(f, "mosaic.html"))
    os.remove("mosaic.html")
    return rv

@command
async def google(msg, content, cmd="google"):
    """
    searches google
    required params:
        <search queary>
    aliases:
        g
        google
    added: 9/10/2020
    """
    if " ip " in content or "my ip" in content: return await returnMsg("no")
    content = Content(content)
    request = requests.get(f"https://www.google.com/search?q={content}").text
    soup = bs.BeautifulSoup(request, features="html.parser")
    results = soup.find_all("div", {"class": "ZINbbc xpd O9g5cc uUPGi"})
    embed = discord.Embed(title="Search Results", color=random.randint(0, 16777215))
    for result in results:
        if result.find("h2", {"class": "wITvVb"}): continue
        try:
            title = result.find_all("div", {"class": "BNeawe vvjwJb AP7Wnd"})[0].text
            desc = result.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})[0].text
            href = result.find_all('a')[0].get("href")
            href = "/url?q=".join("&sa=".join(str(href).split("&sa=")[:-1]).split("/url?q=")[1:])
        except Exception as e:
            print(e)
            continue
        embed.add_field(name=title, value=f'**{href}**\n{desc}')
    return await returnMsg(msg, embed=embed)
