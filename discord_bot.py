from common import *
from cmds import *

CMDS = {
    "echo": echo,
    "iq": iq, 
    "magicball": magicBall, 
    "8ball": magicBall, 
    "7ball": magicBall,   
    "level": level,   
    "rank": level,   
    "lvl": level,   
    "top": leaderboard, 
    "leaderboard": leaderboard, 
    "levels": leaderboard, 
    "lb": leaderboard,   
    "timers": timers, 
    "ping": ping, 
    "help": hlp, 
    "commandusage": cmdUsage, 
    "cmduse": cmdUsage, 
    "cmdusage": cmdUsage, 
    "commanduse": cmdUsage,   
    "findans": calc,
    "equation": calc, 
    "result": calc, 
    "eval": calc, 
    "calc": calc,   
    "shrug": shrug, 
    "spam": spamCmd, 
    "randomface": randomFace,  
    "randface": randomFace,   
    "rface": randomFace,   
    "mmoney": mmoney,   
    "mymoney": mmoney,   
    "money": mmoney,  
    "bal": mmoney,   
    "ucodechar": unicodeChar, 
    "unicodechar": unicodeChar,   
    "serveremote": serverEmote, 
    "doesnothing": writeRoles, 
    "spacer": spacer, 
    "upperlower": upperLower, 
    "ul": upperLower,   
    "rps": startRPS, 
    "rockpaperscissors": startRPS,   
    "complexmessage": complexMessage, 
    "message": complexMessage,   
    "sanity": sanity, 
    "coin": coin, 
    "roleinfo": roleInfo, 
    "rand": rand, 
    "rolecount": roleCount, 
    "comproles": compareRoles, 
    "compareroles": compareRoles,   
    "family": family, 
    "mballreply": mballreply, 
    "8brdel": mballDel, 			
    "count": count, 
    "choose": choose, 
    "mballreplylist": mball,   
    "8ballreplylist": mball,  
    "8breplylist": mball,   
    "8brlist": mball,   
    "piglatin": pigLatin, 
    "igpayatinlay": pigLatin,   
    "mostroles": mostRoles, 
    "clear": clear, 
    "color": color, 
    "servericon": serverIcon, 
    "cc": channelInfo,
    "channelcreated": channelInfo,
    "channelinfo": channelInfo,
    "ci": channelInfo,  
    "changes": changes, 					
    "hex": hexBinOct,
    "bin": hexBinOct,
    "oct": hexBinOct,  
    "response": response, 
    "stopwatch": stopwatch, 
    "timer": stopwatch,  
    "lvlmsg": levelMessage, 
    "emoteinfo": emoteInfo, 
    "clearinvites": ridInvites, 
    "typefor": typeFor, 
    "hangman": hangman, 
    "sendblank": sendBlank, 
    "serverinfo": serverInfo, 
    "pokemon": pokemon, 
    "userinfo": userInfo, 
    "msginfo": messageInfo,
    "messageinfo": messageInfo,
    "fetchrole": fetchSomething, 
    "categoryinfo": categoryInfo, 
    "alphabet": alphabet,   
    "alpha": alphabet,   
    "beta": alphabet,   
    "gamma": alphabet,   
    "delta": alphabet,   
    "epsilon": alphabet,   
    "zeta": alphabet,   
    "eta": alphabet,   
    "theta": alphabet,   
    "iota": alphabet,   
    "kappa": alphabet,   
    "lambda": alphabet,  
    "mu": alphabet,   
    "nu": alphabet,   
    "xi": alphabet,   
    "omicron": alphabet,   
    "pi": alphabet,   
    "rho": alphabet,   
    "sigma": alphabet,   
    "tau": alphabet,   
    "upsilon": alphabet,   
    "phi": alphabet,   
    "chi": alphabet,   
    "psi": alphabet,   
    "omega": alphabet,   
    "spamstop": spamStop, 
    "hypixelpc": hypixelPlayerCount,
    "hppc": hypixelPlayerCount,
    "hypixelbans": hypixelBanStats,
    "hpbans": hypixelBanStats,  
    "hasrole": whoHasRole, 
    "whohas": whoHasRole,   
    "db": INIT_deathBattle,
    "deathbattle": INIT_deathBattle, 
    "shop": shop, 
    "buyitem": buyItem,
    "buy": buyItem,
    "inv": inventory,
    "inventory": inventory,
    "items": inventory,  
    "duplicator": duplicator,
    "duplicate": duplicator,
    "luckynumber": luckynumber,
    "uptime": uptime,
    "weightedcoin": weightedCoin,
    "edit": editCmd,
    "pingresponse": pingResponse,
    "status": setStatus,
    "imginfo": imageInfo,
    "rotate": rotateImg,
    "mirror": mirrorImg,
    "spreadpixels": spreadPixels, 
    "spreadpix": spreadPixels, 
    "filterimg": filterImg,
    "pixelcolor": pixelColor,
    "pxcolor": pixelColor, 
    "shrink": shrinkImg,
    "resize": resizeImg,
    "enhance": enhanceImg,
    "crop": cropImg,
    "imgborder": imgBorder,
    "greyscale": greyscale,
    "grayscale": greyscale, 
    "invert": invert,
    "newimg": newImg,
    "rectangle": rectangle,
    "rect": rectangle,
    "imgtext": imgText,
    "imgarc": imgArc,
    "ellipse": ellipse,
    "imgpoint": point,
    "line": line,
    "polygon": polygon,
    "polyg": polygon,
    "poly": polygon,
    "compileimg": compileImgs,
    "combineimg": compileImgs,
    "addimg": compileImgs, 
    "colorize": colorize,
    "imgdiff": imgDiff,
    "lightimg": lightImg,
    "darkimg": darkImg,
    "imgnoise": imgNoise,
    "convertimg": convertImg,
    "sortimg": sortImg,
    "imgband": imgBand,
    "fileinfo": fileInfo,
    "embedtotext": embedInfo,
    "textinfo": textInfo,
    "ytdl": ytdl,
    "piracyisbad": ytdl,
    "botmods": botMods,
    "embed": embedCmd,
    "emoteusage": emoteUsage,
    "tok": toKelvin,
    "guessinggame": guessingGame,
    "fetchuser": fetchSomething,
    "fetchchannel": fetchSomething,
    "fetchemote": fetchSomething,
    "fetchemoji": fetchSomething
}

@client.event
async def on_ready():
    global blueCheck, neutral, CATS, CMDLIST, CUSTOMCMDS, BOTMODS
    await client.change_presence(activity=discord.Game(f'version: {VERSION}'))
    foo = await client.fetch_user(334538784043696130)
    await foo.send(f"ONLINE\nversion: {VERSION}")
    del foo
    blueCheck = discord.utils.get(client.emojis, name="Blue_check")
    neutral = discord.utils.get(client.emojis, name="neutral")
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    BOTMODS = reloadBOTMODS()
    print(f"ONLINE\nversion: {VERSION}")

async def runBotModCmd(msg, content, cmd):
    global CUSTOMCMDS, CATS, CMDLIST, BOTMODS
    if isBot(msg, client): return
    if cmd == "ADDMONEY" and msg.author.id == EUROID:
        user = await getUserInContent(msg, content.split(", ")[0], cmd)
        amnt = content.split(", ")[1]
        await addMoney(user, float(amnt))
        return await msg.channel.send(f'{float(amnt)} removed from {user.name}')

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

    elif cmd == "ENDPLS" and str(msg.author.id) in BOTMODS.keys():
        if cmd in BOTMODS[str(msg.author.id)]:
            await msg.channel.send("Logging out")
            await client.logout()
            return
    elif cmd == "BAN" and str(msg.author.id) in BOTMODS.keys():
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

    elif cmd == "UNBAN" and str(msg.author.id) in BOTMODS.keys():
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

    elif cmd == "CHANGELVLMSG" and str(msg.author.id) in BOTMODS.keys():
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

    elif cmd == "CHANGEPR" and str(msg.author.id) in BOTMODS.keys():
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

    return await msg.channel.send("you cannot do that")

async def runCommand(msg, content, cmd, layer=1, Iscmd=False, DoFirst=False):
    global CUSTOMCMDS, CATS, CMDLIST, BOTMODS
    DOFIRST = f'--{layer} ' #DEPRICATED
    if DOFIRST in content: #DEPRICATED
        c = await runCommand(msg, content.split(DOFIRST)[1], splitContent(content, DOFIRST, index=1).split(" ")[0][1:], layer=layer + 1, DoFirst=True) #DEPRICATED
        await c.delete() #DEPRICATED
        content = f'{content.split(f" {DOFIRST}")[0]} {c.content}'#DEPRICATED
        msg = c #DEPRICATED
        layer += 1 #DEPRICATED 


    if "/{" in content and "\\" != content[content.index("/{") - 1] and "cmd/{" not in content:
        while True:
            cmds = [x.split("}")[0] for x in content.split("/{")]
            if not cmds: break
            cmds.reverse()
            cmds = cmds[:-1]
            try: cmd = cmds[0]
            except IndexError: break
            mssg = await runCommand(msg, f'{PREFIX}{cmd.strip("_")}', cmd=cmd.split(" ")[0].strip().strip("_"), DoFirst=True)
            await mssg.delete()
            content = content.replace("/{" + cmd + "}", mssg.content)
        return await runCommand(msg, f'{content}', content.split(" ")[0][1:])


    if "cmd/{" in content:
        content = content.replace("cmd/{", "/{")

    with open(commandusageFilePath, "r+") as j:
        data = json.load(j)
        try: data[cmd] += 1
        except: data[cmd] = 1
        clearFile(j)
        json.dump(data, j)

    if cmd.isupper():
        return await runBotModCmd(msg, content, cmd)

    elif cmd == "bans":
        if not testInContent(content, "--raw"):
            with open(bannedFilePath, "r+") as bannedJ:
                data = json.load(bannedJ)
                mssg = "".join([f'{(await client.fetch_user(int(user))).name}: {data[user]}\n' for user in data.keys()])
                try: return await msg.channel.send(mssg)
                except: pass
        with open(bannedFilePath, "rb") as bannedJ:
            return await msg.channel.send(file=discord.File(bannedJ, "bans.json"))

    elif cmd == "if":
        res = await calc(msg, content.split("{")[0].strip(), cmd, ReturnRes=True)
        content = "{".join(content.split("{")[1:])
        if res:
            for cmd in content.split(";"):
                if cmd.strip() == "}": break
                content = await runCommand(msg, cmd.strip(), cmd.strip().split(" ")[0].strip().strip(PREFIX))

    elif "\;" in content and "--notyet" not in content:
        content = Content(content, removeCmd=False)
        content.calcOps()
        content = content.string
        for cmd in content.split("\;"):
            print(cmd)
            content = await runCommand(msg, cmd.strip(), cmd.strip().split(" ")[0].strip().strip(PREFIX))
    elif "--notyet" in content:
        content = content.replace("--notyet", "")
    case = CMDS.get(cmd)
    
    if case:
        content = await case(msg, content, cmd=cmd)
        Iscmd = True
    else:
        case = switch(cmd).start()
        if case("tof"): content = await oneLineCmd(msg, 9 / 5 * float(splitContent(content, cmd + " ", index=1)) + 32)
        elif case("avatar"): content = await oneLineCmd(msg, (await getUserInContent(msg, content, cmd)).avatar_url)
        elif case("toc"): content = await oneLineCmd(msg, 5 / 9 * (float(splitContent(content, cmd + " ", index=1)) - 32))
        elif case(["thepenguincommand", "tpc", "thewavecommand", "twc"]): content = await oneLineCmd(msg, random.choice(("very nice!", "very cool!", "<:TiredPuffle:707773683854213140>")))
        elif case("reverse"): content = await oneLineCmd(msg, splitContent(content, f'{cmd} ')[1][::-1])
        elif case("imscared"): content = await oneLineCmd(msg, random.choice(("don't be :smiling_imp:", "oh it's ok :)))))))))))))))))", "just don't pay attention of the sounds coming from your attic.....\nit's ok", "it's ok... he's comming :)")))
        elif case("doihavecovid"): content = await oneLineCmd(msg, "yes" if random.random() < .995 else "no")
        elif case(["ship", "boat", "boip"]): content = await oneLineCmd(msg, "DISCLAIMER: I DO NOT SUPPORT SHIPPING PEOPLE IN ANY WAY, HOWEVER MY MASTER SEEMS TO HAVE OTHER PLANS" if random.random() >= .985 else f'{splitContent(content, ", ")[0].replace("[" + cmd + " ", "")[0:len(splitContent(content, ", ")[0].replace("[" + cmd + " ", "")) // 2]}{splitContent(content, ", ")[1][len(splitContent(content, ", ")[1]) // 2:]}')
        elif case(["ttc", "thetroycommand"]): content = await oneLineCmd(msg, random.choice(("meow", "7", "**7**", "*7*", "mo", "<:TiredPuffle:707773683854213140>", "nnn")))
        elif case("longmessage"): content = await oneLineCmd(msg, "```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````hI```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
        elif case(["wiki", "wikipedia"]): content = await oneLineCmd(msg, f'https://en.wikipedia.org/wiki/Special:Search?search={content[len(cmd) + 2:].replace(" ", "_")}')
        elif case("upupdowndownleftrightleftright"):
            return await msg.channel.send("what do you think this is some arcade machine with secret codes, lol")
        elif case(["eccmd", "editcustomcmd"]):
            content = await editCustomCmd(msg, content, cmd=cmd)
            CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
        elif case(["customcmd", "accmd", "customcommand"]): 
            content = await addCustomCmd(msg, content, cmd=cmd)
            CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
        elif case(["removecustomcmd", "delcustomcmd", "dccmd", "rccmd"]): 
            content = await removeCustomCmd(msg, content, cmd=cmd)
            CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
        elif case("customcmdlist"): await customCmdList(msg, content, cmd=cmd)
        elif case(list(CUSTOMCMDS.keys())): 
            content = Content(CUSTOMCMDS[cmd], removeCmd=False)
            content.formatMessage(msg)
            content = content.string.strip()
            while True:
                cmds = [x.split("}")[0] for x in content.split("{")]
                if "if" in content: break
                cmds.reverse()
                cmds = cmds[:-1]
                try: cmd = cmds[0]
                except IndexError: break
                mssg = await runCommand(msg, f'{PREFIX}{cmd.strip("_")}', cmd=cmd.split(" ")[0].strip().strip("_"), DoFirst=True)
                await mssg.delete()
                content = content.replace("{" + cmd + "}", mssg.content)
            content = await oneLineCmd(msg, content)
        case.end()
        Iscmd = True

    if cmd not in CMDLIST and not Iscmd: 
        with open(commandusageFilePath, "r+") as j:
            data = json.load(j)
            del data[cmd]
            clearFile(j)
            json.dump(data, j)
        content = await msg.channel.send(f'{cmd} {random.choice(("is not a thing", "does not exist"))}')
    return content

@client.event
async def on_message(msg):
    global Stop, playingGuessingGame
    global blueCheck, neutral
    content = msg.content
        
    if "[timeit" in content:
        timeThisMessageTime = time.time()
        TimeThisMessage = True
        content = content.replace("[timeit", "").strip()
    else: TimeThisMessage = False
    Iscmd = False
    if msg.author.id == 311621977339068418 and msg.channel.id not in (732071485564256377, 715043261110288415):
        await msg.delete()
    if "[" in content and PREFIX != content[0]:
        if "[delete" in content: 
            await msg.delete() #deletes message if requested or myustiak sent it
        elif "[delin" in content:
            t = content.split("[delin")[1]
            try: await asyncio.sleep(float(t))
            except: return await msg.channel.send("NaN")
            await msg.delete()
            Iscmd = True
        elif "[rw" in content and "[dr" not in content:
            c = splitContent(content, s, index=1).strip()
            if " " in c:
                split = splitContent(c, " ")
                for s in split:
                    if s in client.emojis: await msg.add_reaction(discord.utils.get(client.emojis, id=int(s.split(":")[2][:-1])))
                    else: await msg.add_reaction(s)
            else:
                e = discord.utils.get(client.emojis, id=int(c.split(":")[2][:-1])) if c in client.emojis else c
                await msg.add_reaction(e)
            Iscmd = True
    if not content: 
        return
        
    if (msg.channel.id == 427973752647712768 or (f'{PREFIX}chkx' in content and "[dr" not in content)):
        await msg.add_reaction(blueCheck)
        await msg.add_reaction(neutral)
        await msg.add_reaction("❌")
        Iscmd = True

    if random.random() >= .9995: 
        if isBot(msg, client): return
        await msg.channel.send(random.choice(("mhm", "interesting", "fascinating", "very cool")))

    if f"<@!{client.user.id}>" in content and client.user.id not in playingHangman.keys():
        await msg.channel.send(random.choice((discord.utils.find(lambda e: e.name.lower() == "watching1", client.emojis), discord.utils.find(lambda e: e.name.lower() == "pinged", client.emojis))))
        
    await giveXP(msg)
    await reduceXP(msg)

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

    if "<:" in content and ">" in content:
        emotes = re.findall(r'<:[A-Za-z-_]{1,100}:[0-9]{18}>', str(content))
        if emotes and not msg.author.bot:
            with open(emoteUsageFilePath, "r+") as j:
                data = json.load(j)
                for emote in emotes:
                    emoteId = re.findall(r'[0-9]{18}', emote)[0]
                    try: data[str(emoteId)] += 1
                    except: data[str(emoteId)] = 1
                clearFile(j)
                json.dump(data, j)

    if content[0] in PREFIX:

        cmd = getCmd(content)

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
        if not cmd: return
        WriteToFile = False

        if " --delete" in content: 
            content = content.replace("--delete", "")
            await msg.delete()

        if " --cmddelete" in content:
            content = content.replace("--cmddelete", " --delete")

        if testInContent(content, ">>> "):
            WriteToFile = splitContent(content, ">>> ")[1]
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
            return

        elif cmd == "reactiontime":
            await msg.channel.send("i will say GO and you have to send something as fast as possible (probably prepare the message before hand)")
            await asyncio.sleep(random.uniform(1.5, 6))
            start = time.time()
            await msg.channel.send("GO")
            try: await client.wait_for("message", check=lambda message: message.author == msg.author, timeout=60.0)
            except asyncio.TimeoutError: return await msg.channel.send(f"{msg.author} ran out of time to react")
            else: 
                end = time.time()
                return await msg.channel.send(f'your reaction time {end - start}')
        else: 
            content = await runCommand(msg, content, cmd, Iscmd=Iscmd)
            if WriteToFile:
                await writeToFile(msg, content.content, WriteToFile)
                await content.delete()
                
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

    if TimeThisMessage: return await msg.channel.send(f'it took {time.time() - timeThisMessageTime} process the message')

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
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        role = discord.utils.get(member.guild.roles, name="vc")
        await member.add_roles(role)
    elif before.channel and not after.channel:
        role = discord.utils.get(member.guild.roles, name="vc")
        await member.remove_roles(role)

client.run(token)