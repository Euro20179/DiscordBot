from common import *

command.setCategory("info", "commands that give info")

@command
async def pokemon(msg, content, cmd="pokemon"):
    """
    gets info on a pokemon
    required params:
        <pokemon or pokedex number>: the pokemon to get info on
    added: 6/2/2020
    """
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

@command
async def weather(msg, content, cmd="weather"):
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
    with open("epicfile.html", "w") as f:
        f.write(request.text)
    try:
        soup = bs.BeautifulSoup(request.text, features="html.parser")
        tempurature = soup.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})[-1].text.split("°")[0]
        warning = None
        if "\n" in tempurature:
            tempurature, *warning = tempurature.split("\n")[::-1]
            warning = "\n".join(warning)
        temp = int(tempurature)
        condition = soup.find_all("div", {"class": "BNeawe tAd8D AP7Wnd"})[0].text
        condition = condition.split("AM" if "AM" in condition else "PM")[1]
        location = soup.find_all("span", {"class": "BNeawe tAd8D AP7Wnd"})[0].text
        celcius = f'{5 / 9 * (float(tempurature.split("°")[0]) - 32)}°C'
    except Exception as e:
        print(e)
        return await returnMsg(msg, "failed")
    if "Pleasanton, CA" in location: return await returnMsg(msg, "failed")
    r = int(255 * ((temp) / 134))
    b = int(0 + (1 - (temp / 134)) * 255)
    embed = discord.Embed(title=location, color=discord.Color.from_rgb(r, 0, b))
    embed.add_field(name="Current weather (F)", value=tempurature)
    embed.add_field(name="Current weather (C)", value=celcius)
    if warning: embed.add_field(name="Warning", value=warning, inline=False)
    embed.add_field(name="Overhead", value=condition, inline=False)
    return await returnMsg(msg, content="the tempurature which is probably too hot or smth stop being so picky smh" if random.random() > .01 else None, embed=embed)

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
    added: 7/10/2020
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
async def whoHasRole(msg, content, cmd="hasrole"):
    """
    gives a list of members with a role
    required params:
        <role>: the role to check
    options:
        --file: puts the results in a file
    aliases:
        whohasrole
        hasrole
        whohas
    added: 6/11/2020
    """
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

@command
async def textInfo(msg, content, cmd="textinfo"):
    """
    gives info on text
    required params:
        <text/file> (the text in the file can be more than the discord limit of 2k chars)
    options:
        -re <regex>: search the text with a regex
        --rankwords: gives a list of the most used words
    added: 7/7/2020
    """
    text = Content(content)
    sep = " "
    try:
        _, filename, url = await getImg(msg, NotFromChat=True)
        await saveImg(filename, url)
        with open(filename, "r") as f:
            text = Content(f.read(), removeCmd=False)
    except:
        pass
    for op, param in text.opsWithParams():
        if op in ("-re", "-regex"):
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
    words = {}
    for word in text.split():
        try:
            words[word] += 1
        except:
            words[word] = 1
    sortedWords = sorted(words.items(), key=lambda x: x[1], reverse=True)
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
                mssg = await returnMsg(msg, file=discord.File(f, "text.txt"))
            os.remove(f'{msg.author.id}.txt')
            return mssg
    return await returnMsg(msg, embed=embed)

@command
async def categoryInfo(msg, content, cmd="categoryinfo"):
    """
    gets info on a category
    required params:
        <category>: the category to get info on
    added: 6/3/2020
    """
    content = Content(content).string
    cat = discord.utils.find(lambda x: x.name.lower() == content.lower(), msg.guild.categories)
    embed = discord.Embed(title=cat.name)
    embed.add_field(name="id", value=cat.id)
    embed.add_field(name="position", value=cat.position)
    embed.add_field(name="channels", value=len(cat.channels))
    embed.add_field(name="text channels", value=len(cat.text_channels))
    embed.add_field(name="voice channels", value=len(cat.voice_channels))
    embed.add_field(name="created at", value=formatDateTime(cat.created_at))
    return await returnMsg(msg, embed=embed)

@command
async def emoteInfo(msg, content, cmd="emoteinfo"):
    """
    gives info about a serveremote
    required params:
        <emote>: the emote to get info on
    added: 5/30/2020
    """
    emote = await msg.guild.fetch_emoji(int(content.split(":")[2][:-1]))
    embed = discord.Embed(title=emote.name)
    embed.set_thumbnail(url=emote.url)
    embed.add_field(name="Animated", value=emote.animated)
    embed.add_field(name="Added by", value=emote.user)
    embed.add_field(name="created at", value=formatDateTime(emote.created_at))
    embed.add_field(name="id", value=emote.id)
    embed.add_field(name="Image", value=str(emote.url))
    embed.add_field(name="raw mention", value=f"\<:{emote.name}:707773683854213140>")
    return await returnMsg(msg, embed=embed)

@command
async def messageInfo(msg, content, cmd="messageinfo"):
    """
    gets info on a message, the one you just sent by default
    optional params:
        [message id [channel]]: the message to get info on
            if it is in a different channel, specify the channel
    aliases:
        msginfo
        messageinfo
    added: 6/3/2020
    """
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
    embed.add_field(name="created at", value=formatDateTime(msg.created_at))
    embed.add_field(name="jump to link", value=msg.jump_url)

    return await returnMsg(msg, embed=embed)

@command
async def serverInfo(msg, content, cmd="serverinfo"):
    """
    gets info on the server
    added: 6/2/2020
    """
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
    embed.add_field(name="creation time", value=formatDateTime(creation))
    embed.add_field(name="age", value=t - creation)
    return await returnMsg(msg, embed=embed)

@command
async def userInfo(msg, content, cmd="userinfo"):
    """
    gets info on user
    optional params:
        [user]: the user to get info on, defaults to you
    added: 6/3/2020
    """
    user = (await getUserInContent(msg, content, cmd))
    embed = discord.Embed(title=user.name, color=user.color)
    embed.add_field(name="Join date", value=formatDateTime(user.joined_at))
    embed.add_field(name="nick name", value=user.nick)
    embed.add_field(name="color", value=f'RGB: {", ".join(tuple(str(x) for x in user.color.to_rgb()))}\nhex: {user.color}')
    embed.add_field(name="role count", value=len(user.roles))
    embed.add_field(name="avatar url", value=user.avatar_url)
    embed.add_field(name="created at", value=formatDateTime(user.created_at))
    embed.add_field(name="discriminator", value=user.discriminator)
    embed.add_field(name="id", value=user.id)
    embed.add_field(name="mention", value=user.mention)
    embed.add_field(name="raw mention", value="\\" + user.mention)
    embed.add_field(name="roles", value=" ".join([x.mention for x in user.roles]), inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    return await returnMsg(msg, embed=embed, allowedmentions=discord.AllowedMentions(roles=False,everyone=False,users=False))

@command
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
        embed.add_field(name="Created at", value=formatDateTime(role.created_at))
        return await returnMsg(msg, embed=embed)
    except AttributeError:
        return await returnMsg(msg, "role not found")

@command
async def fileInfo(msg, content, cmd="fileinfo"):
    """
    gets info on a file
    required params:
        <file>
    added: 7/7/2020
    """
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

@command
async def roleCount(msg, content, cmd="rolecount"):
    """
    gives the role count of [member] defaults to you
    optional params:
        [member]: the member to get the role count of
    options:
        --showroles: whether or not to show the roles the user has
    added: 1/19/2020
    """
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
            return await returnMsg(msg, embed=embed, allowedmentions=discord.AllowedMentions(everyone=False,users=False,roles=False))    
        else: return await returnMsg(msg, roleCount)
    else: return await returnMsg(msg, "User not found")

@command
async def compareRoles(msg, content, cmd="compareroles"):
    """
    compares the roles of 2 members
    required params:
        <member1 | member 2>: the 2 members seperate with |
    aliases:
        comproles
        compareroles
    added: 5/5/2020
    """
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

@command
async def mball(msg, content, cmd="8ball"):
    """
    the list of 8ball replies
    aliases:
        mballreplylist
        8ballreplylist
        8breplylist
        8brlist
    added: 5/12/2020
    """
    with open(mballresponseFilePath, "rb") as f:
        return await returnMsg(msg, file=discord.File(f, "mballresponse.txt"))

@command
async def mostRoles(msg, content, cmd="mostroles"):
    """
    gives the [top] members by role count
    optional params:
        [top]: the amount to list, defaults to 5
    added: 1/1/2020
    """
    content = Content(content).split(" ")[0]
    top = int(content) if content else 5
    memberRoles = {member.display_name.split("#")[0]: len(member.roles) - 1 for member in msg.guild.members}
    sortedKeys = sorted(memberRoles, key=memberRoles.get, reverse=True)
    top = [f'{r}, {memberRoles[r]}' for n, r in enumerate(sortedKeys) if n < top]
    return await returnMsg(msg, "\n".join(top))

@command
async def color(msg, content, cmd="color"):
    """
    gives the color of [role]
    or the hex color of [r, g, b]
    or the rgb of [#colorcode]
    optional params:
        [role]: the role to get color of, defaults to your top role
        OR
        [r, g, b]: the r, g, b to get the hex code of
        OR
        [#hexcode]: the hexcode to get the rgb of
        OR
        [user]: the user to get the color of
    options:
        --rand: picks a random color
    added: 5/11/2020
    """
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
        c = random.randint(0, 16777215)

    if "#" in c:
        c = c.replace("#", "")
        r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:], 16)
        embed = discord.Embed(title=f'{r} {g} {b}', color=discord.Color(int(c, 16)))
        return await returnMsg(msg, embed=embed)

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

@command
async def channelInfo(msg, content, cmd="cc"):
    """
    gives info about the current channel
    optional params:
        [channel]: the channel to get info about
    aliases:
        channelinfo
        ci
        cc
    added: 5/26/2020
    """
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
        embed.add_field(name="days till last pin", value=str(daysTillLastPin))
    embed.add_field(name="Created at", value=formatDateTime(created))
    embed.add_field(name="Pins", value=pinCount)
    embed.add_field(name="time since creation", value=diff)
    embed.add_field(name="id", value=channel.id)
    embed.add_field(name="position", value=channel.position + 1)
    embed.add_field(name="slowmode delay", value=channel.slowmode_delay)
    embed.add_field(name="mention", value=channel.mention)
    embed.add_field(name="raw mention", value="\\" + channel.mention)
    return await returnMsg(msg, embed=embed)

@command
async def hypixelPlayerCount(msg, content, cmd="hypixelpc"):
    """
    CUSTOM:
```gets hypixel's current player count
or the playercount of a gametype if specified``````optional params:
    [gametype]: the gametype to get player count of``````md
GAMES:
#main lobby
#tournament lobby
#duels
#prototype
#speed uhc
#replay
#legacy
#skyblock
#mcgo
#pit
#build battle
#murder mystery
#tntgames
#battleground
#survival games
#skywars
#walls3
#ardcade
#uhc
#bedwars
#housing
#super smash
#limbo
#idle
#queue``````aliases:
hypixelplayercount
hppc
hypixelpc``````added: 6/9/2020```
    """
    game = Content(content).string
    if game:
        data = requests.get(f"https://api.hypixel.net/gameCounts?key={HPKEY}").json()
        if game == "list":
            return await returnMsg(msg, ", ".join(list(x.lower() for x in data["games"].keys())))
        gameData = data["games"].get(game.upper().replace(" ", "_"))
        if gameData:
            embed = discord.Embed(title=game, color=discord.Color(0xffff00))
            embed.add_field(name=game, value=gameData["players"])
            modes = gameData.get("modes")
            if modes:
                for mode in modes.items():
                    embed.add_field(name=mode[0], value=mode[1])
            return await returnMsg(msg, embed=embed)
    return await returnMsg(msg, requests.get(f"https://api.hypixel.net/playercount?key={HPKEY}").json()["playerCount"])

@command
async def hypixelBanStats(msg, content, cmd="hypixelban"):
    """
    gets the hypixel ban stats
    aliases:
        hypixelbanstats
        hypixelbans
        hpbans
    added: 6/22/2020
    """
    data = requests.get(f"https://api.hypixel.net/watchdogstats?key={HPKEY}").json()
    embed = discord.Embed(title="ban stats", color=discord.Color(0xffff00))
    for k, v, in data.items():
        if k == "success": continue
        else: embed.add_field(name=k, value=v)
    return await returnMsg(msg, embed=embed)

@command
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
        else:
            data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=False if content.testOps("--least", "--ltg") else True)}
            send = "\n".join([f'{n + 1}: {c[0]}, {c[1]}' for n, c in enumerate(data.items()) if n < top])
            try:
                clearFile(j)
                json.dump(data, j)
                return await returnMsg(msg, send)
            except: return await returnMsg(msg, "too long of a message")

@command
async def hlp(msg, content, cmd="help"):
    """
    help command
    optional params:
        [category/cmd]: list the cmds in a particular category if a category is given
            otherwise gives help for command
    options:
        --raw: gets the raw json file of the cmds
        --file: generates a file instead of embed if [category] is specified
    aliases:
        help
        hlp
    added: day 1
    """
    global CUSTOMCMDS
    CUSTOMCMDS = await reloadCMDSLIST()
    CATS = await reloadCMDSLIST(retCats=True)
    content = Content(content)
    if content @ "--raw":
        with open(cmdJsonFilePath, "rb") as f:
            return await returnMsg(msg, file=discord.File(f, cmdJsonFilePath))
    elif not content:
        embed = discord.Embed(title="Help", color=discord.Color(random.randint(0, 16777215)))
        with open(cmdJsonFilePath, "r") as j:
            data = json.load(j)
            for cat, catI in data.items():
                embed.add_field(name=cat, value=catI["desc"])
        return await returnMsg(msg, embed=embed)
    else:
        if content.string.upper().strip() in CATS and content.string.strip() != "custom":
            with open(cmdJsonFilePath, "r") as j:
                data = json.load(j)
                for cat, catI in data.items():
                    if cat.lower().strip() == content.lower().strip():
                        embed = discord.Embed(title=catI["desc"], color=discord.Color(random.randint(0, 16777215)))
                        field = "```\n"
                        n = 0
                        for n, cmd in enumerate(catI["cmds"]):
                            if n % 7 == 0 and n != 0: 
                                field += f'{cmd}```'
                                embed.add_field(name=str(n), value=field)
                                field = "```\n"
                            else:
                                field += f'{cmd}\n'
                        if n % 7 != 0:
                            embed.add_field(name=str(n), value=field + "```")
                        return await returnMsg(msg, embed=embed)

        elif content.string.strip() == "custom":
            return await returnMsg(msg, "do [ccmdlist")

        elif CUSTOMCMDS.get(str(content)):
            with open(customcmdsFilePath) as j:
                data = json.load(j)
                embed = discord.Embed(title=str(content), color=discord.Color(random.randint(0, 16777215)))
                for cmd in data:
                    if cmd["name"] == str(content):
                        params = cmd.get("params")
                        date = cmd.get("date")
                        Locked = cmd.get("Locked")
                        addedBy = cmd.get("addedby")
                        editedBy = cmd.get("editedby")
                        embed.add_field(name="desc", value=cmd["desc"])
                        if params: embed.add_field(name="params", value=params, inline=False)
                        if date: embed.add_field(name="date added", value=date, inline=False)
                        if Locked: embed.add_field(name="locked", value=Locked, inline=False)
                        if addedBy:
                            embed.add_field(name="added by", value=(await client.fetch_user(int(addedBy))).mention, inline=False)
                        if editedBy:
                            embed.add_field(name="edited by", value="\n".join([(await client.fetch_user(int(user))).mention for user in editedBy]), inline=False)
                        return await returnMsg(msg, embed=embed)
                return await returnMsg(msg, "cmd not found")
        else:
            try: return await returnMsg(msg, CMDS[str(content)].help())               
            except KeyError as e:
                return await returnMsg(msg, f'{content} does not exist {":face_with_monocle:"*10}')                 

@command
async def changes(msg, content, cmd="changes"):
    """
    gives the latest changes
    optional params:
        [version]: the version to see changes for
    options:
        -date <date> (-m/-day/-y/-dy): the date to get the versions of
        --raw: the raw txt file
    added: 5/20/2020
    """
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

@command
async def uptime(msg, content, cmd="uptime"):
    """
    gives the bot's uptime
    optional params:
        [unit]: the unit of time to get, can be:
            seconds, minutes, hours, days, weeks
    added: 6/26/2020
    """
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

@command
async def prfile(msg, content, cmd="prfile"):
    """
    gets the file of ping responses
    aliases:
        prfile
        prlist
        pingresponselist
        pingresponsefile
    added: 8/18/2020
    """
    for user in RAMUserInfo.values():
        await user.dumpPingResponseInfo()
    with open(pingResponseFilePath, "rb") as f:
        return await returnMsg(msg, file=discord.File(f, "pingResponse.json"))

@command
async def imgInfo(msg, content, cmd="imginfo"):
    """
    gets info on an image
    required params:
        <img>
    added: 7/4/2020
    """
    att, *_ = await getImg(msg)

    embed = discord.Embed(title=att.filename if att.filename else "UNKNOWN.img")
    embed.add_field(name="id", value=att.id if att.id else "UNKOWN")
    embed.add_field(name="file size", value=att.size if att.size else "UNKOWN")
    embed.add_field(name="width", value=att.width if att.width else "UNKOWN")
    embed.add_field(name="height", value=att.height if att.height else "UNKOWN")
    embed.add_field(name="url", value=att.url if att.url else "UNKOWN")
    embed.add_field(name="spoiler?", value=att.is_spoiler if type(att.is_spoiler) is bool else "UNKNOWN")
    return await returnMsg(msg, embed=embed)

@command
async def bans(msg, content, cmd="bans"):
    """
    gets the bans
    """
    for user in RAMUserInfo.values():
        await user.dumpBannedInfo()
    if not testInContent(content, "--raw"):
        with open(bannedFilePath, "r+", encoding="utf-8-sig") as bannedJ:
            data = json.load(bannedJ)
            mssg = "".join([f'{(await client.fetch_user(int(user))).name}: {" ".join(data[user])}\n' for user in data.keys() if data[user]])
            try: return await returnMsg(msg, mssg)
            except: pass
    with open(bannedFilePath, "rb") as bannedJ:
        return await returnMsg(msg, file=discord.File(bannedJ, "bans.json"))

@command
async def botMods(msg, content, cmd="botmods"):
    """
    lists the botmods, and the perms they have
    optional parmas:
        [user]: the user to check perms of
    """
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    content = Content(content)
    if content @ "--raw":
        with open(botModsFilePath, "rb") as f:
            return await returnMsg(msg, file=discord.File(f, "botmods.json"))
    with open(botModsFilePath, "r", encoding="utf-8-sig") as j:
        data = json.load(j)
        if content:
            try: return await returnMsg(msg, "\n".join(data.get(str(content.getUser(msg).id))))
            except: return await returnMsg(msg, "None")
        else: return await returnMsg(msg, "\n".join([f'{await getUserInContent(msg, "ok " + k, "ok")}: {", ".join(i)}' for k, i in BOTMODS.items()]))

@command
async def timers(msg, content, cmd="timers"):
    """
    gets a list of timers that are currently running
    options:
        --raw: the file
    """
    embed = discord.Embed(title="Timers")
    for user in RAMUserInfo.values():
        await user.dumpTimerInfo()
    if "--raw" in content:
        with open(timersPath, "r") as f:
            return await returnMsg(msg, file=discord.File(f, "timers.json"))
    with open(timersPath, "r", encoding="utf-8-sig") as tJ:
        data = json.load(tJ)
        for user, t in data.items():
            user = await client.fetch_user(user)
            embed.add_field(name=user.name, value=round(time.time() - t, 2))
        return await returnMsg(msg, embed=embed)

@command
async def population(msg, content, cmd="population"):
    """
    gets the population of a place
    required params:
        <place>: the place to get the population of
    aliases:
        pop
        population
    options:
        -wm [year]: uses worldmeters instead of google
            year gets that particular year, defaults to latest
            year is in incroments of 5 starting in 1955
            the name of the country must be the name the website gave it, so this may be more challenging
    added: 8/20/2020
    """
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-wm":
            year = param if param else str(datetime.datetime.now().year)
            search = content.string.strip().lower()
            request = requests.get(f'https://www.worldometers.info/world-population/{search.replace(" ", "-")}-population/')
            if request.status_code == 404:
                return await returnMsg(msg, f"{content} not found check your spelling")
            request = request.text
            soup = bs.BeautifulSoup(request, features="html.parser")
            table = soup.find("table", {"class": "table table-striped table-bordered table-hover table-condensed table-list"})
            head = table.find_all("thead")[0]
            th = {n: name.text for n, name in enumerate(head.find_all("th"))}
            body = table.find_all("tbody")[0]
            data = {}
            for row in body.find_all("tr"):
                currYear = 0
                for n, td in enumerate(row.find_all("td")):
                    if n == 0: currYear = td.text
                    if currYear != year: continue
                    else: data[th[n]] = td.text
                if data: break
            embed = discord.Embed(title=f'Population of {search}')
            for name, value in data.items():
                embed.add_field(name=name, value=value)
            return await returnMsg(msg, embed=embed)
    content = content.string
    request = requests.get(f'https://www.google.com/search?q={content.replace(" ", "+")}+population').text
    soup = bs.BeautifulSoup(request, features="html.parser")
    soup = soup.find("div", {"class": "BNeawe iBp4i AP7Wnd"}).text
    pop = " ".join(soup.split(" ")[:-1])
    time = soup.split(" ")[-1]
    embed = discord.Embed(title=f'Population of {content}')
    embed.add_field(name="population", value=pop)
    if time: embed.add_field(name="when", value=time)
    return await returnMsg(msg, embed=embed)

@command
async def prefixes(msg, content, cmd="prefixes"):
    """
    lists the prefixes
    added: 8/31/2020
    """
    with open(prefixFilePath, "r") as f:
        return await returnMsg(msg, "```" + f.read() + "```")
        
@command
async def define(msg, content, cmd="define"):
    """
    searches https://dictionary.com for a definition
    required params:
        <word>
    aliases:
        define
        definition
        dictionary
        def
    added: 9/1/2020
    """
    content = cutCmd(content)

    colors = {
        "red": 0xff0000,
        "green": 0x00ff00,
        "blue": 0x0000ff,
        "yellow": 0xffff00,
        "orange": 0xff9900,
        "purple": 0x8206e8,
        "pink": 0xfca9e2,
        "lime": 0x25fc00
    }

    embed = discord.Embed(title=f"Definition of {content}", color=random.randint(1, 16777215) if not colors.get(content) else colors[content])
    embed.set_footer(text=f"https://www.dictionary.com/browse/{content}")
    request = requests.get(f"https://www.dictionary.com/browse/{content}").text
    try:
        english = bs.BeautifulSoup(request, features="html.parser").find("div", {"class": "css-1urpfgu e16867sm0"}) #there's a brittish version TODO: implement it

        sound = english.find("span", {"class": "pron-spell-content css-z3mf2 evh0tcl2"})
        embed.add_field(name="pronounciation", value=sound.text)
        ipa = english.find("span", {"class": "pron-ipa-content css-z3mf2 evh0tcl2"})
        embed.add_field(name="ipa pronounciation", value=ipa.text)

        sections = english.find_all("section", {"class": "css-pnw38j e1hk9ate0"})
        for section in sections:
            partOfSpeach = section.find_all("h3", {"class": "css-sdwj8v e1hk9ate1"})[0].text.strip()
            for n, definition in enumerate(section.find_all("span", {"class": "one-click-content css-1p89gle e1q3nk1v4"}), 1):
                embed.add_field(name=f'{partOfSpeach}, {n}:', value=definition.text)
        return await returnMsg(msg, embed=embed)
    except:
        return await returnMsg(msg, f'ERROR: probably not found')

@command
async def getuserid(msg, content, cmd="getuserid"):
    """
    gets the user's id based on name
    required params:
        *<user> (sep with |)
    aliases:
        getuserid
        userid
    added: 9/3/2020
    """
    content = Content(content)
    sep = "\n"
    for op, param in content.opsWithParams():
        if op == "-sep":
            sep = Content.whitespaceFormat(param)
    users = tuple(str(Content(user.strip(), removeCmd=False).getUser(msg).id) for user in content.split("|") if user)
    return await returnMsg(msg, sep.join(users))