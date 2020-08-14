from cmds import *
from common import __version__

@client.event
async def on_ready():
    global blueCheck, neutral, CUSTOMCMDS, BOTMODS
    await client.change_presence(activity=discord.Game(f'version: {__version__}'))
    foo = await client.fetch_user(334538784043696130)
    await foo.send(f"ONLINE\nversion: {__version__}")
    del foo
    blueCheck = discord.utils.get(client.emojis, name="Blue_check")
    neutral = discord.utils.get(client.emojis, name="neutral")
    CUSTOMCMDS = await reloadCMDSLIST()
    BOTMODS = reloadBOTMODS()
    print(f"ONLINE\nversion: {__version__}")

@client.event
async def on_disconnect():
    with open(commandusageFilePath, "w") as j:
        json.dump(commandUsage, j)

async def runBotModCmd(msg, content, cmd):
    global CUSTOMCMDS, BOTMODS
    if isBot(msg, client): return
    if cmd == "ADDMONEY" and msg.author.id == EUROID:
        user = await getUserInContent(msg, content.split(", ")[0], cmd)
        amnt = content.split(", ")[1]
        await addMoney(user, float(amnt))
        return await msg.channel.send(f'{float(amnt)} removed from {user.name}')

    elif cmd == "RESETEMOJIUSAGE" and msg.author.id == EUROID:
        with open(emoteUsageFilePath, "w") as f:
            f.write("{}")
        return await msg.channel.send("reset")

    elif cmd == "RESETCMDUSAGE" and msg.author.id == EUROID:
        with open(commandusageFilePath, "w") as f:
            f.write("{}")
        return await msg.channel.send("reset")

    elif cmd == "ALLOW" and msg.author.id == EUROID:
        user = await getUserInContent(msg, content.split("|")[0], cmd)
        with open(botModsFilePath, "r+") as f:
            data = json.load(f)
            if str(user.id) in data.keys():
                data[str(user.id)].append(content.split("|")[1].strip())
            else:
                data[str(user.id)] = [content.split("|")[1].strip()]
            clearFile(f)
            json.dump(data, f)
            await msg.channel.send(f'{user.name} can now use {content.split("|")[1]}')
            BOTMODS = reloadBOTMODS()
            return
    elif cmd == "DISALLOW" and msg.author.id == EUROID:
        user = await getUserInContent(msg, content.split("|")[0], cmd)
        with open(botModsFilePath, "r+") as f:
            data = json.load(f)
            if str(user.id) in data.keys():
                data[str(user.id)].remove(content.split("|")[1].strip())
            clearFile(f)
            json.dump(data, f)
            await msg.channel.send(f'{user.name} can not use {content.split("|")[1]}')
            BOTMODS = reloadBOTMODS()
            return

    elif cmd == "ENDPLS" and await hasPerms(str(msg.author.id), cmd):
        if cmd in BOTMODS[str(msg.author.id)]:
            await msg.channel.send("Logging out")
            await client.logout()
            return

    elif cmd == "BAN" and await hasPerms(str(msg.author.id), cmd):
        if cmd in BOTMODS[str(msg.author.id)]:
            user = await getUserInContent(msg, " ".join(content.split(" ")[0:2]), cmd)
            banFrom = splitContent(content, " ", index=2)
            with open(bannedFilePath, "r+") as bannedJ:
                data = json.load(bannedJ)
                if data.get(str(user.id)):
                    data[str(user.id)].append(banFrom)
                else: data[str(user.id)] = [banFrom]
                clearFile(bannedJ)
                json.dump(data, bannedJ)
                return await msg.channel.send(f'banned {user.name} from {banFrom}')

    elif cmd == "UNBAN" and await hasPerms(str(msg.author.id), cmd):
        if cmd in BOTMODS[str(msg.author.id)]:
            user = await getUserInContent(msg, " ".join(content.split(" ")[0:2]), cmd)
            unbanFrom = splitContent(content, " ", index=2)
            with open(bannedFilePath, "r+") as bannedJ:
                data = json.load(bannedJ)
                if data.get(str(user.id)):
                    data[str(user.id)].remove(unbanFrom)
                else: return await msg.channel.send("did not find user")
                clearFile(bannedJ)
                json.dump(data, bannedJ)
                return await msg.channel.send(f'unbanned {user.name} from {unbanFrom}')

    elif cmd == "CHANGELVLMSG" and await hasPerms(str(msg.author.id), cmd):
        if cmd in BOTMODS[str(msg.author.id)]:
            user = await getUserInContent(msg, content, cmd)
            with open(levelingDataFilePath, "r+") as j:
                data = json.load(j)
                try:
                    await msg.channel.send("to what?") 
                    changeTo = await client.wait_for("message", check=lambda message: message.author.id == msg.author.id, timeout=60.0)
                except: return await msg.channel.send("failed")
                userData = data[str(user.id)]
                userData["message"] = changeTo.content
                clearFile(j)
                json.dump(data, j)
                return await msg.channel.send("changed")

    elif cmd == "CHANGEPR" and await hasPerms(str(msg.author.id), cmd):
        if cmd in BOTMODS[str(msg.author.id)]:
            user = await getUserInContent(msg, content, cmd)
            with open(pingResponseFilePath, "r+") as j:
                data = json.load(j)
                try:
                    await msg.channel.send("to what?") 
                    changeTo = await client.wait_for("message", check=lambda message: message.author.id == msg.author.id, timeout=60.0)
                except Exception as e: 
                    print(e)
                    return await msg.channel.send("failed")
                if changeTo.content.lower() == "none":
                    del data[str(user.id)]
                else:
                    if data.get(str(user.id)):
                        data[str(user.id)]["response"] = changeTo.content
                    else:
                        data[str(user.id)] = {"response": changeTo.content, "when": ["offline"]}
                clearFile(j)
                json.dump(data, j)
                return await msg.channel.send("changed")

    return await msg.channel.send("you cannot do that or the command doesn't exist who knows")

async def runCommand(msg, content, cmd, Iscmd=False, DoFirst=False, WriteToFile=False):
    global CUSTOMCMDS, BOTMODS, commandUsage

    if "/{" in content and "\\" != content[content.index("/{") - 1] and "cmd/{" not in content:
        while True:
            if len(content.split("{")) != len(content.split("}")):
                return await msg.channel.send("syntax error missing { or }")
            cmds = [x.split("}")[0] for x in content.split("/{")]
            if not cmds: break
            cmds.reverse()
            cmds = cmds[:-1]
            try: cmd = cmds[0]
            except IndexError: break
            mssg = await runCommand(msg, f'{PREFIX}{cmd.strip("_")}', cmd=cmd.split(" ")[0].strip().strip("_"), DoFirst=True)
            if mssg.embeds and "userinfo" not in cmd:
                content = content.replace("/{" + cmd + "}", (await embedToReadableDict(msg, msg.embeds)).content)
            else: content = content.replace("/{" + cmd + "}", str(mssg.content))
        return await runCommand(msg, f'{content}', getCmd(content))

    if "cmd/{" in content:
        content = content.replace("cmd/{", "/{")

    try: commandUsage[cmd] += 1
    except: commandUsage[cmd] = 1

    if cmd.isupper() and (await hasPerms(str(msg.author.id), cmd) or msg.author.id == EUROID):
        return await runBotModCmd(msg, content, cmd)
        
    elif cmd == "if":
        if Content(content) @ "--help":
            return await returnMsg(msg, """
it's an if statement
    required params:
        <expr>(
            *<cmds>;
        )
        [else](
            *<cmds>;
        )
        must be in that syntax, else is optional, all the cmds in else trigger if the normal <expr> didn't
        each command must be seperated by ;
    added: 7/17/2020
                """
            )
        if Content(content.split("(")[0].strip()).suitibleForEval():
            res = await calc(msg, content.split("(")[0].strip(), cmd, ReturnRes=True)
        else: return await returnMsg(msg, "nice try")
        content = "(".join(content.split("(")[1:])
        if res:
            for cmd in content.split(";"):
                if cmd.strip()[0] == ")": break
                content = await runCommand(msg, cmd.strip(), cmd.strip().split(" ")[0].strip().strip(PREFIX), DoFirst=True)
        elif not res and "else" in content:
            elseStmnt = content.split(")")[-2].strip() + ")"
            expr = Content(elseStmnt.split("(")[0])
            content = "(".join(elseStmnt.split("(")[1:])
            for cmd in content.split(";"):
                if cmd.strip() == ")": break
                content = await runCommand(msg, cmd.strip(), cmd.strip().split(" ")[0].strip().strip(PREFIX), DoFirst=True)
        Iscmd = True

    elif cmd == "for":
        content = Content(content)
        if content @ "--help":
            return await returnMsg(msg, """
it's a for loop
it'll break if it lasts longer than 1 min 30 seconds
    required params:
        <times>(
            *<cmds>;
        )
        must be in that syntax
        it does all the commands seperated by ;
        times times
    added: 7/23/2020
                """
            )
        times = content.split("(")[0]
        stuff = content.strip(f'{times}(').strip().split(";")
        res = []
        timeoutLength = 90
        startTimeout = time.time()
        for i in range(int(times)):
            for cmd in stuff:
                cmd = cmd.replace("{i}", str(i))
                if cmd == ")": break
                content = await runCommand(msg, f'{PREFIX}{cmd.strip()}', cmd.strip().split(" ")[0], DoFirst=True) 
                res.append(str(content.content))
            if (time.time() - startTimeout) > timeoutLength: break
        content = await returnMsg(msg, "\n".join(res))       
        Iscmd = True

    elif ";;" in content and "--notyet" not in content:
        content = Content(content, removeCmd=False)
        content.calcOps()
        content = content.string
        for cmd in content.split(";;"):
            print(cmd)
            await runCommand(msg, cmd.strip(), cmd.strip().split(" ")[0].strip().strip(PREFIX))
        Iscmd = True

    elif "--notyet" in content:
        content = content.replace("--notyet", "")
    
    case = CMDS.get(cmd)
    if case and not Iscmd:
        if Content(content) @ "--help":
            content = await returnMsg(msg, case.help())
        else: content = await case(msg, content, cmd=cmd)
        Iscmd = True
    elif not case:
        startContent = content
        secretCmds = {
            "upupdowndownleftrightleftrightba": lambda: returnMsg(msg, "what do you think this is some arcade machine with secret codes, lol")
        }
        if secretCmds.get(cmd):
            content = await secretCmds[cmd]()
        elif cmd == "exec" and await hasPerms(msg.author.id, "exec"):
            try:
                exec(str(Content(content)), globals(), locals())
                content = await returnMsg(msg, "done")
            except Exception as e:
                content = await returnMsg(msg, e)
            Iscmd = True
        elif cmd in ["eccmd", "editcustomcmd"]:
            content = await editCustomCmd(msg, content, cmd=cmd)
            CUSTOMCMDS = await reloadCMDSLIST()
        elif cmd in ["customcmd", "accmd", "customcommand"]: 
            content = await addCustomCmd(msg, content, cmd=cmd)
            CUSTOMCMDS = await reloadCMDSLIST()
        elif cmd in ["removecustomcmd", "delcustomcmd", "dccmd", "rccmd"]: 
            content = await removeCustomCmd(msg, content, cmd=cmd)
            CUSTOMCMDS = await reloadCMDSLIST()
        elif cmd in ["customcmdlist", "ccmdlist"]: content = await customCmdList(msg, content, cmd=cmd)
        elif cmd in CUSTOMCMDS.keys(): 
            content = str(Content(CUSTOMCMDS[cmd], removeCmd=False).formatMessage(msg, ret=True)).strip()
            while True:
                if len(content.split("{")) != len(content.split("}")):
                    return await msg.channel.send("syntax error missing { or }")
                cmds = [x.split("}")[0] for x in content.split("{")]
                cmds.reverse()
                cmds = cmds[:-1]
                try: cmd = cmds[0]
                except IndexError: break
                mssg = await runCommand(msg, f'{PREFIX}{cmd.strip("_")}', cmd=cmd.split(" ")[0].strip().strip("_"), DoFirst=True)
                if mssg.embeds and "userinfo" not in cmd:
                    content = content.replace("{" + cmd + "}", (await embedToReadableDict(msg, msg.embeds)).content)
                else: content = content.replace("{" + cmd + "}", str(mssg.content))
            content = await returnMsg(msg, content)
        if content != startContent:
            Iscmd = True
    if not Iscmd: 
        del commandUsage[cmd]
        content = await returnMsg(msg, f'{cmd} {random.choice(("is not a thing", "does not exist"))}')
    
    if not DoFirst and content: 
        if WriteToFile:
            if content.embeds:
                content.content = (await embedToReadableDict(msg, msg.embeds)).content
            await writeToFile(msg, content.content, WriteToFile)
        elif content.embeds:
            return await msg.channel.send(embed=content.embeds if content.embeds else None, tts=content.tts)
        elif content.attachments:
            return await msg.channel.send(file=content.attachments if content.attachments else None, tts=content.tts)
        else:
            try: return await msg.channel.send(content.content, tts=content.tts)
            except discord.errors.HTTPException:
                await msg.channel.send("too long here's a file")
                with open("file.txt", "w", encoding="utf-8", errors="ignore") as f:
                    f.write(str(content.content))
                with open("file.txt", "rb") as f:
                    msg = msg.channel.send(file=discord.File(f, f'{cmd}.txt'))
                os.remove("file.txt")
                return await msg

    else: return content

@client.event
async def on_message(msg):
    global Stop
    global blueCheck, neutral
    content = msg.content
        
    if f"{PREFIX}timeit" in content:
        timeThisMessageTime = time.time()
        TimeThisMessage = True
        content = content.replace(f"{PREFIX}timeit", "").strip()
    else: TimeThisMessage = False
    Iscmd=RWhenDone = False
    if msg.author.id == 311621977339068418 and msg.channel.id not in (732071485564256377, 715043261110288415):
        await msg.delete()
    if PREFIX in content and PREFIX != content[0]:
        cmd = content.split(PREFIX)[1].split(" ")[0]
        with switch(cmd) as case:
            if case("delete"): await msg.delete()
            elif case("delin"):
                t = content.split(f"{PREFIX}delin")[1]
                try: await asyncio.sleep(float(t))
                except: return await returnMsg(msg, "NaN")
                await msg.delete()
                Iscmd = True
            elif case("rw") and not case(["dr", "rwd"]):
                c = splitContent(content, f"{PREFIX}rw", index=1).strip()
                if " " in c:
                    split = splitContent(c, " ")
                    for s in split:
                        if s in client.emojis: await msg.add_reaction(discord.utils.get(client.emojis, id=int(s.split(":")[2][:-1])))
                        else: await msg.add_reaction(s)
                else:
                    e = discord.utils.get(client.emojis, id=int(c.split(":")[2][:-1])) if c in client.emojis else c
                    await msg.add_reaction(e)
            elif case("rwd") and not case("dr"):
                RWhenDone=Iscmd = True
            Iscmd = True
    if not content: 
        return
        
    if (msg.channel.id == 427973752647712768 or (f'{PREFIX}chkx' in content and f"{PREFIX}dr" not in content)):
        await msg.add_reaction(blueCheck)
        await msg.add_reaction(neutral)
        await msg.add_reaction("❌")
        Iscmd = True

    if random.random() >= .9995: 
        if isBot(msg, client): return
        await msg.channel.send(random.choice(SARCASTICQUOTES))

    if f"<@!{client.user.id}>" in content and client.user.id not in playingHangman.keys():
        await msg.channel.send(random.choice((discord.utils.find(lambda e: e.name.lower() == "watching1", client.emojis), discord.utils.find(lambda e: e.name.lower() == "pinged", client.emojis))))

    if msg.mentions and not isBot(msg, client):
        usersPinged = {str(user.id) for user in msg.mentions}
        with open(pingResponseFilePath, "r") as j:
            data = json.load(j)
            for user in usersPinged & set(data.keys()):
                if data.get(user):
                    u = findMember(user, msg)
                    if str(u.status) in data[user]["when"] or "all" in data[user]["when"]:
                        c = Content(data[user]["response"], removeCmd=False)
                        c = c.formatMessage(msg, ret=True)
                        await msg.channel.send(c)     

    if content[0] in PREFIX:

        cmd = getCmd(content)
        content = content.replace("—", "--")

        if "<<<" in content:
            f = msg.attachments[0]
            filename, url = f.filename, f.url
            await saveImg(filename, url)
            with open(filename, "r") as f:
                read = f.read()
            content = content.replace("<<<", read)
            msg.attachments = []
            os.remove(filename)

        if msg.attachments and cmd not in ["imginfo", "fileinfo"]:
            content += " " + " ".join(att.url for att in msg.attachments)
        WriteToFile = False

        if " --delete" in content: 
            content = content.replace("--delete", "")
            await msg.delete()

        if " --cmddelete" in content:
            content = content.replace("--cmddelete", "--delete")

        if ">>>" in content:
            WriteToFile = splitContent(content, ">>>")[1]
            content = content.replace(f">>> {WriteToFile}", "")

        if msg.mention_everyone:
            return await msg.channel.send("NO")

        if msg.author.id:
            with open(bannedFilePath, "r") as bannedJ:
                data = json.load(bannedJ)
                if data.get("EVERYONE"):
                    if cmd in data["EVERYONE"]:
                        return await msg.channel.send(f"no one can use {cmd}")
                userData = data.get(str(msg.author.id))
                if userData:
                    if cmd in userData or "ALL" in userData:
                        return await msg.channel.send(f"You cannot use {cmd}")

        if cmd == "stop":
            await stop()
            
        else: content = await runCommand(msg, content, cmd, Iscmd=Iscmd, WriteToFile=WriteToFile)
                
    if playingHangman.get(msg.author.id):
        tempWord = playingHangman[msg.author.id]["word"]
        if content in ["QUIT", "STOP", "CANCEL", "END"]:
            del playingHangman[msg.author.id]
            return await msg.channel.send(f'{msg.author.mention} CANCELLED\nthe word was {tempWord}')
        tempLives = playingHangman[msg.author.id]["lives"]
        tempDisp = playingHangman[msg.author.id]["disp"]
        tempGuessed = playingHangman[msg.author.id]["guessed"]
        content = content.lower()
        if content.lower() == tempWord.lower():
            del playingHangman[msg.author.id]
            return await msg.channel.send(f'{msg.author.mention} YOU WIN')
        if len(content) != 1:
            return
        if content in tempGuessed:
            return await msg.channel.send(f'you already said {content}')
        tempGuessed.append(content)
        if content.lower() in tempWord.lower():
            foo = [x for x in tempDisp]
            for n, w in enumerate(tempWord):
                if content.lower() == w.lower():
                    foo[n] = w
            tempDisp = "".join(foo)
        else:
            tempLives -= 1
        if tempLives <= 0 and tempDisp == tempWord:
            del playingHangman[msg.author.id]
            return await msg.channel.send(f"ITS A DRAW\nThe word was {tempWord}\n{msg.author} ran out of lives but guessed the word")
        elif tempLives <= 0:
            del playingHangman[msg.author.id]
            return await msg.channel.send(f'YOU LOSE\nThe word was {tempWord}')
        elif tempDisp == tempWord:
            del playingHangman[msg.author.id]
            return await msg.channel.send(f'YOU WIN\nYou won with {tempLives} left!')
        else: await msg.channel.send(f'{msg.author.mention}\nLives left: {tempLives}\nKnown word: {tempDisp}\nguesses: {" ".join(tempGuessed)}')
        playingHangman[msg.author.id] = {"word": tempWord, "lives": tempLives, "disp": tempDisp, "guessed": tempGuessed}

    if not msg.content:
        msg.content = "None"
    if "<:" in msg.content and ">" in msg.content:
        emotes = re.findall(r'<:[A-Za-z-_0-9]{1,100}:[0-9]{18}>', str(content))
        if emotes and not msg.author.bot:
            with open(emoteUsageFilePath, "r+") as j:
                data = json.load(j)
                for emote in emotes:
                    emoteId = re.findall(r'[0-9]{18}', emote)[0]
                    try: data[str(emoteId)] += 1
                    except: data[str(emoteId)] = 1
                clearFile(j)
                json.dump(data, j)

    await giveXP(msg)
    await reduceXP(msg)
    if TimeThisMessage: await msg.channel.send(f'it took {time.time() - timeThisMessageTime} process the message')
    if RWhenDone: await msg.add_reaction("❌")

@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.is_custom_emoji():
        with open(emoteUsageFilePath, "r+") as j:
            data = json.load(j)
            try: data[str(payload.emoji.id)] += 1
            except: data[str(payload.emoji.id)] = 1
            clearFile(j)
            json.dump(data, j)

@client.event
async def on_message_edit(before, after):
    await on_message(after)

@client.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        role = discord.utils.get(member.guild.roles, name="vc")
        await member.add_roles(role)
    elif before.channel and not after.channel:
        role = discord.utils.get(member.guild.roles, name="vc")
        await member.remove_roles(role)

client.run(token)