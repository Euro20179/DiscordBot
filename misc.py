from common import *


@command
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

@command
async def embedToText(msg, content, cmd="embedtotext"):
    """
    makes an embed into text, why idk
    required params:
        <embed>
    options:
        --json: instead of text to python dictionary
    added: 7/7/2020
    """
    content = Content(content).string
    fetchFrom = msg.channel
    if msg.channel_mentions:
        fetchFrom = msg.channel_mentions[0]
        content = content.replace(fetchFrom.mention,  "").strip()
    if not content.isnumeric():
        return await returnMsg(msg, "not a number")
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

@command
async def editMsg(msg, content, cmd="editmsg"):
    """
    edits a message the blue circle sent
    required params:
        <content of new message>
    options:
        -channel <channel>: the channel the message was sent in
        --nodel: doesn't delete your command message
        --delmsg: deletes the message you are editing
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
    if content @ "--delmsg":
        await msg.delete()
    else:
        repWith.formatMessage(msg, {"{msg}": msg.content})
        repWith = repWith.whitespaceFormat(str(repWith))
        await msg.edit(content=repWith)

@command
async def ytdl(msg, content, cmd="ytdl"):
    """
    piracy is bad.
    required params:
        <youtube url>: the url :)
    aliases:
        piracyisbad
        ytdl
    added: 7/7/2020
    """
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
            return rv

@command
async def setStatus(msg, content, cmd="status"):
    """
    sets the bots status to something
    required params:
        <message>
    aliases:
        status
        setstatus
    added: 7/2/2020
    """
    st = Content(content)
    if len(st) >= 1:
        await client.change_presence(activity=discord.Game(name=str(st)))
        return await returnMsg(msg, f"changed to {st}")
    else: return await returnMsg(msg, "you didn't set the status to anything")

@command
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
        abc
        SECRET:
        gamma
        delta
        epsilon
        zeta
        eta
        theta
        iota
        kappa
        lambda
        mu
        nu
        xi
        omicron
        pi
        rho
        sigma
        tau
        upsilon
        phi
        chi
        psi
        omega
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

@command
async def doesnothing(msg, content, cmd="doesnothing"):
    """
    does absolutely nothing :)
    required params:
        <text>
    added: 1/1/2020
    """
    filename = Content(content)
    with open(f"{filename}.txt", "w") as f:
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

@command
async def mballreply(msg, content, cmd="mballreply"):
    """
    adds <reply> to the list of possibly 8ball replies, you must have
    perms to be able to use this
    required params:
        <reply>: the response
    FORMATS (question)
    added: 1/29/2020
    """
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    mssg = Content(content)
    if str(msg.author.id) in BOTMODS.keys():
        if cmd in BOTMODS[str(msg.author.id)]:
            with open(mballresponseFilePath, "a") as f:
                f.write(mssg + "\n")
            return await returnMsg(msg, "message added")
    else: return await returnMsg(msg, "you don't have perms")

@command
async def stopwatch(msg, content, cmd="stopwatch"):
    """
    starts a stopwatch if not started, otherwise gets the time
    optional params:
        [inverval [round]]: the interval of time to show
            can be seconds, minutes, hours, days, or weeks
            [round]: the places to round to
    aliases:
        timer
        stopwatch
    added: 5/20/2020
    """
    content = Content(content)
    userInfo: UserInfo = RAMUserInfo[msg.author.id]
    running = userInfo.time
    stopAt = content.toSet() & {"seconds", "minutes", "hours", "days", "weeks"}
    if not running:
        userInfo.time = time.time()
        return await returnMsg(msg, f'{msg.author.mention} stopwatch started')
    elif running and content @ "--stop":
        t = await formatSeconds(time.time() - running)
        await msg.channel.send(embed=discord.Embed(title=str(round(t[0], 2)) + f' {t[1]}'))
        userInfo.time = 0
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

@command
async def avatarCmd(msg, content, cmd="avatar"):
    """
    gets the avatar of you
    optional params:
        [user]: the user to get the avtar of
    """
    return await returnMsg(msg, (await getUserInContent(msg, content, cmd)).avatar_url)

@command
async def count(msg, content, cmd="count"):
    """
    counts in #counting, can be said in any channel
    optional params:
        [fancy]: the styling of the text
            ex: \**
    options:
        -e (-c <color>): makes it an embed
            -c <color>: specifies the color to use defaults to black
        --(any combination of i, u, and b): i makes it *italisized*
            b makes it **bold**
            u makes it __underlined__
        --all: is the same as --iub
        --tts: makes it tts
        --ret: gives the number back and sends it in the 
            origional chat you sent if it's not #counting
    added: 5/6/2020
    """
    try: await msg.delete()
    except: pass
    content = Content(content)
    channel = discord.utils.get(msg.guild.channels, name="counting")
    highest = int(max([x.content.replace("*", "").replace("_", "").replace("`", "").replace("\\", "").strip(".") async for x in channel.history(limit=1)])) + 1
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
    mssg = None
    for op, param in content.opsWithParams():
        if op == "-e":
            if param: color = int(param, 16)
            else: color = 0x000000
            mssg = await channel.send(embed=discord.Embed(title=f'.{highest}.', color=discord.Color(color)))
    if content:
        fancy = content.strip()
    text = fancy + text + fancy[::-1]
    if not mssg: mssg = await channel.send(text, tts=content @ "--tts")
    if msg.channel != channel and content @ "--ret": return await returnMsg(msg, mssg.content, embed=mssg.embeds[0] if mssg.embeds else None)

@command
async def fetchrole(msg, content, cmd="fetchrole"):
    """
    gets the name of role ids
    required params:
        *<role id>
    added: 6/3/2020
    """
    content = Content(content)
    fetches = [msg.guild.get_role(int(x.strip())).name for x in content.split(" ")]
    return await returnMsg(msg, "\n".join(fetches))

@command
async def fetchuser(msg, content, cmd="fetchuser"):
    """
    fetches the user by user id
    required params:
        *<userid>
    added: 5/30/2020
    """
    content = Content(content)
    fetches = [(await client.fetch_user(int(x.strip()))).name for x in content.split(" ")]
    return await returnMsg(msg, "\n".join(fetches))

@command
async def fetchchannel(msg, content, cmd="fetchchannel"):
    """
    fetches the channel by id
    required params:
        *<channelid>
    added: 7/1/2020
    """
    content = Content(content)
    fetches = [(await client.fetch_user(int(x.strip()))).mention for x in content.split(" ")]
    return await returnMsg(msg, "\n".join(fetches))

@command
async def fetchemote(msg, content, cmd="fetchemote"):
    """
    fetches the channel by id
    required params:
        *<channelid>
    aliases:
        fetchemote
        fetchemoji
    added: 7/10/2020
    """
    content = Content(content)
    fetches = [(await msg.guild.fetch_emoji(int(x.strip()))).name for x in content.split(" ")]
    return await returnMsg(msg, "\n".join(fetches))

@command
async def imscared(msg, content, cmd="imscared"):
    """
    be terrified :)
    aliases:
        SECRET:
        i'mscared
    """
    msgs = (
        "don't be :smiling_imp:", 
        "oh it's ok :)))))))))))))))))", 
        "just don't pay attention of the sounds coming from your attic.....\nit's ok", 
        "it's ok... he's comming :)"
        )
    return await returnMsg(msg, random.choice(msgs))

@command
async def doihavecovid(msg, content, cmd="doihavecovid"):
    """
    CUSTOM:
    ```diff
-maybe who knows hopefuly yo do
-i mean don't have covid :))))))```
    """
    r = random.random() < .995
    return await returnMsg(msg, f'{"yes"*r}{"no"*(r^1)}') #someone said if statements were too slow, but this is really challenging to read lmao

@command
async def typeFor(msg, content, cmd="type"):
    """
    makes the bot type for a specified time
    defaults to 5 seconds
    optional params:
        [time]: the time to type
    options:
        --nosend: doesn't say "done" when it's done
    added: 6/1/2020
    """
    content = Content(content)
    Send = not content @ "--nosend"
    timeToType = float(content.strip()) if content.strip() else 5
    if timeToType > 420:
        return await returnMsg(msg, "sorry thats too long")
    async with msg.channel.typing():
        await asyncio.sleep(timeToType)
    return await returnMsg(msg, f'typed for {timeToType} seconds') if Send else msg

@command
async def spamStop(msg, content, cmd="spamstop"):
    """
    spams [stop 10 times
    abuse of this command will get you banned from it
    """
    for _ in range(10):
        await msg.channel.send(f'{PREFIXES[0]}stop')
        await asyncio.sleep(random.uniform(.3, 1.2))

@command
async def pingResponse(msg, content, cmd="pingresponse"):
    """
    when someone pings you (except bots) it will say this message
    required params:    
        <message>: the message to say
        OR
        -WHEN <offline/online/idle/dnd/all>: this controls when it triggers
            by default it's when you're offline
            you can change it with this
            do any combination of them
    added: 7/1/2020
    """
    response = Content(content)
    if isBot(msg, client): return
    userInfo: UserInfo = RAMUserInfo[msg.author.id]
    if "-WHEN" in response:
        when = response.split("-WHEN ")[1]
        when = when.split(" ")
        userInfo.pingResponseWhen = when
    elif response.lower() == "none":
        userInfo.pingRespone = ""
    else:
        userInfo.pingResponse = str(response)
    if "-WHEN" in response:
        return await returnMsg(msg, f'response will happen when you are {" ".join(userInfo.pingResponseWhen)}')
    return await returnMsg(msg, f"changed to:\n{response}")

@command
async def wait(msg, content, cmd="wait"):
    """
    idk waits? lol
    required params:
        <wait time>: the amount of time to wait
    """
    content = Content(content)
    try: t = float(content)
    except: return await returnMsg("not a number")
    await asyncio.sleep(t)
    
@command
async def quote(msg, content, cmd="quote"):
    """
    puts a message into the quotes channel,
    and it mentions the user and says what channel
    required params:
        <message id> (must be in the channel you are in)
    added: 8/13/2020
    """
    content = Content(content)
    NoDel = content @ "--nodel"
    messageToQuote = await msg.channel.fetch_message(int(content))
    quotesChannel = await client.fetch_channel(693641312531906661)
    await quotesChannel.send('> {0.content}\n{0.author.mention} - {0.channel.mention}'.format(messageToQuote))
    if not NoDel: await msg.delete()

@command
async def nice(msg, content, cmd="nice"):
    """
    nice
    aliases:
    SECRET:
    69
    added: 8/14/2020
    """
    if Content(content).strip() != "nice":
        return await returnMsg(msg, "incorrect password")
    else:
        await msg.author.send("you have earned the secret trophy very n i c e")

@command
async def wikipediaCmd(msg, content, cmd="wiki"):
    """
    generates the url link for a wikipedia page
    required params:
        *<search> (sep with |)
    options:
        -sep <seperator>: what to seperate each link by
    aliases:
        wiki
        wikipedia
        wikipediacmd
        SECRET:
        knowledge
    """
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-sep":
            sep = Content.whitespaceFormat(param)
            break
    else: sep = "\n"
    queries = frozenset(f'https://en.wikipedia.org/wiki/Special:Search?search={search.strip().replace(" ", "_")}' for search in content.split("|"))
    return await returnMsg(msg, sep.join(queries))

@command
async def sendBlank(msg, content, cmd="sendblank"):
    """
    send a specified amount of lines of blank messages defaults to 5
    optional params:
        [lines]: the amount of blank lines to send
    added: 6/1/2020
    """
    content = Content(content)
    amnt = int(content) if content else 5
    return await returnMsg(msg, "_" + ("\n" * amnt) + "_")

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
async def addPrefix(msg, content, cmd="addprefix"):
    """
    adds a prefix to the list of prefixes,
    mustn't contain spaces
    required params:
        <prefix>
    added: 8/31/2020
    """
    global PREFIXES
    if not await hasPerms(msg.author.id, cmd):
        return await returnMsg(msg, "you don't have perms")
    content = cutCmd(content).strip()
    if content not in PREFIXES:
        with open(prefixFilePath, "a") as f:
            f.write(f"\n{content}")
        PREFIXES.append(content)
        return await returnMsg(msg, f'added {content} as a prefix')
    return await returnMsg(msg, f'already a prefix')

@command
async def removePrefix(msg, content, cmd="removeprefix"):
    """
    removes a prefix
    required params:
        <prefix>
    added: 8/31/2020
    """
    global PREFIXES
    content = cutCmd(content).strip()
    if not await hasPerms(msg.author.id, cmd) or STDPrefix == content:
        return await returnMsg(msg, "you don't have perms and you can't remove the default prefix what is wrong with you")
    with open(prefixFilePath, "r+") as f:
        p = f.read().split("\n")
        p.remove(content)
        clearFile(f)
        f.write("\n".join(p))
    PREFIXES.remove(content)
    return await returnMsg(msg, f"removed prefix: {content}")
    
@command
async def avatar(msg, content, cmd="avatar"):
    """
    gets the avatar of [user] (defaults to you)
    optional params:
        [user]
    aliases:
        avatarurl
        avatar_url
        avatar
    """
    user = Content(content).getUser(msg)
    return await returnMsg(msg, user.avatar_url)