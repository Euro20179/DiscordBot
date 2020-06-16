from common import *
from cmds import *

@client.event
async def on_ready():
    global blueCheck, neutral, CATS, CMDLIST, CUSTOMCMDS
    await client.change_presence(activity=discord.Game(f'version: {VERSION}'))
    foo = await client.fetch_user(334538784043696130)
    await foo.send(f"ONLINE\nversion: {VERSION}")
    del foo
    blueCheck = discord.utils.get(client.emojis, name="Blue_check")
    neutral = discord.utils.get(client.emojis, name="neutral")
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    print(f"ONLINE\nversion: {VERSION}")

async def runCommand(msg, content, cmd, layer=1):
    global CUSTOMCMDS, CATS, CMDLIST
    DOFIRST = f'--{layer} '
    if DOFIRST in content:
        c = await runCommand(msg, content.split(DOFIRST)[1], splitContent(content, DOFIRST, index=1).split(" ")[0][1:], layer=layer + 1)
        await c.delete()
        content = f'{content.split(f" {DOFIRST}")[0]} {c.content}'
        msg = c
        layer += 1

    if "/{" in content:
        temp = list(reversed(content.split("/{")))
        tempCMDSLIST = tuple(x["name"] for x in CMDLIST)
        for n, line in enumerate(temp):
            if n + 1 == len(temp): break
            foo = line.split("}")[0]
            mssg = await runCommand(msg, f'{PREFIX}{foo}', cmd=line.split("}")[0].split(" ")[0].strip())
            await mssg.delete()
            temp[temp.index(line) + 1] += mssg.content
            if line.split("}")[1]:
                temp[-1] += line.split("}")[1]
        content = temp[-1]
        return await runCommand(msg, f'{content}', content.split(" ")[0][1:])

    with open(commandusageFilePath, "r+") as j:
        data = json.load(j)
        try: data[cmd] += 1
        except: data[cmd] = 1
        clearFile(j)
        json.dump(data, j)
        
    if cmd == "timeit":
        start = time.time()
        await runCommand(msg, content.replace(f'{PREFIX}timeit ', ""), splitContent(content, "timeit ", index=1).split(" ")[0][1:])
        return await msg.channel.send(time.time() - start)

    elif cmd == "ENDPLS" and msg.author.id in [EUROID, 412365502112071681]:
        await msg.channel.send("Logging out")
        await client.logout()

    elif cmd == "BANS":
        with open(bannedFilePath, "r+") as bannedJ:
            data = json.load(bannedJ)
            mssg = "".join([f'{(await client.fetch_user(int(user))).name}: {data[user]}\n' for user in data.keys()])
            try: return await msg.channel.send(mssg)
            except: pass
        with open(bannedFilePath, "rb") as bannedJ:
            await msg.channel.send(file=discord.File(bannedJ, "bans.json"))

    elif cmd == "BAN" and msg.author.id in [EUROID, 412365502112071681]:
        user = await getUserInContent(msg, " ".join(content.split(" ")[0:2]), cmd)
        banFrom = splitContent(content, " ", index=2)
        with open(bannedFilePath, "r+") as bannedJ:
            data = json.load(bannedJ)
            if data.get(str(user.id)):
                data[str(user.id)].append(banFrom)
            else: data[str(user.id)] = [banFrom]
            clearFile(bannedJ)
            await msg.channel.send(f'banned {user.name} from {banFrom}')
            json.dump(data, bannedJ)

    elif cmd == "UNBAN" and msg.author.id in [EUROID, 412365502112071681]:
        user = await getUserInContent(msg, " ".join(content.split(" ")[0:2]), cmd)
        unbanFrom = splitContent(content, " ", index=2)
        with open(bannedFilePath, "r+") as bannedJ:
            data = json.load(bannedJ)
            if data.get(str(user.id)):
                data[str(user.id)].remove(unbanFrom)
            else: return await msg.channel.send("did not find user")
            clearFile(bannedJ)
            await msg.channel.send(f'unbanned {user.name} from {unbanFrom}')
            json.dump(data, bannedJ)

    elif cmd == "secretcommand": await msg.channel.send("you have found a SECRET COMMAND do secretcommand + 10 for another command (10 doesn't equal 10 ;) )")
    elif cmd == "secretcommand2": await msg.channel.send("the final clue... save - e + 3")
    elif cmd == "sav3":
        await msg.channel.send("i have been lost for 15 years")
        await asyncio.sleep(1.2)
        await msg.channel.send("and now finally...")
        await asyncio.sleep(.6)
        await msg.channel.send("you have followed the secret clues and awoken me")
        await asyncio.sleep(1.5)
        await msg.channel.send("congratulations to anyone whitnessing this event, you earn a secret role a very epic secret role :) as my gift for saving me")
        return await msg.channel.send("<!@334538784043696130> give them the role smh")

    elif cmd == "upupdowndownleftrightleftright":
        return await msg.channel.send("what do you think this is some arcade machine with secret codes, lol")

    cmds = {
        cmd == "echo": echo,
        cmd == "iq": iq, 
        cmd in ["magicball", "8ball", "7ball"]: magicBall, 
        cmd in ["level", "rank", "lvl"]: level, 
        cmd in ["top", "leaderboard", "levels", "lb"]: leaderboard, 
        cmd == "timers": timers, 
        cmd == "ping": ping, 
        cmd == "help": hlp, 
        cmd in ["commandusage", "cmduse", "cmdusage", "commanduse"]: cmdUsage, 
        cmd in ["findans", "equation", "result", "eval", "calc"]: calc, 
        cmd == "shrug": shrug, 
        cmd == "spam": spamCmd, 
        cmd in ["randomface","randface", "rface"]: randomFace, 
        cmd in ["mmoney", "mymoney", "money", "bal"]: mmoney, 
        cmd in ["ucodechar", "unicodechar"]: unicodeChar, 
        cmd == "serveremote": serverEmote, 
        cmd == "doesnothing": writeRoles, 
        cmd == "spacer": spacer, 
        cmd in ["upperlower", "ul"]: upperLower, 
        cmd in ["rps", "rockpaperscissors"]: startRPS, 
        cmd in ["complexmessage", "message"]: complexMessage, 
        cmd == "sanity": sanity, 
        cmd == "coin": coin, 
        cmd == "roleinfo": roleInfo, 
        cmd == "rand": rand, 
        cmd == "rolecount": roleCount, 
        cmd in ["comproles", "compareroles"]: compareRoles, 
        cmd == "family": family, 
        cmd == "mballreply": mballreply, 
        cmd == "8brdel": mballDel, 			
        cmd == "count": count, 
        cmd == "choose": choose, 
        cmd in ["mballreplylist", "8ballreplylist", "8breplylist", "8brlist"]: mball, 
        cmd in ["piglatin", "igpayatinlay"]: pigLatin, 
        cmd == "mostroles": mostRoles, 
        cmd == "clear": clear, 
        cmd == "color": color, 
        cmd == "servericon": serverIcon, 
        cmd in ["cc", "channelcreated", "channelinfo", "ci"]: channelInfo, 
        cmd == "changes": changes, 					
        cmd in ["hex", "bin", "oct"]: hexBinOct, 
        cmd == "response": response, 
        cmd in ["stopwatch", "timer"]: stopwatch, 
        cmd == "lvlmsg": levelMessage, 
        cmd == "emoteinfo": emoteInfo, 
        cmd == "clearinvites": ridInvites, 
        cmd == "typefor": typeFor, 
        cmd == "hangman": hangman, 
        cmd == "sendblank": sendBlank, 
        cmd == "serverinfo": serverInfo, 
        cmd == "pokemon": pokemon, 
        cmd == "userinfo": userInfo, 
        cmd in ["msginfo", "messageinfo"]: messageInfo, 
        cmd == "fetchrole": fetchRole, 
        cmd == "categoryinfo": categoryInfo, 
        cmd in ["alphabet", "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"]: alphabet, 
        cmd == "spamstop": spamStop, 
        cmd == "covid": covid, 
        cmd == "hypixelpc": hypixelPlayerCount, 
        cmd in ["hasrole", "whohas"]: whoHasRole, 
        cmd in ["db", "deathbattle"]: INIT_deathBattle, 
        cmd == "shop": shop, 
        cmd in ["buyitem", "buy"]: buyItem, 
        cmd in ["inv", "inventory"]: inventory, 
        cmd == "duplicsuccessfully ator": duplicator
    }
    if (case := cmds.get(True)):
        content = await case(msg, content, cmd=cmd)

    elif cmd == "tof": await oneLineCmd(msg, 9 / 5 * float(splitContent(content, cmd + " ", index=1)) + 32)
    elif cmd == "avatar": await oneLineCmd(msg, await getUserInContent(msg, content, cmd)).avatar_url
    elif cmd == "fetchuser": await oneLineCmd(msg, await client.fetch_user(int(splitContent(content, f'{cmd} ', index=1))).name)
    elif cmd == "toc": await oneLineCmd(msg, 5 / 9 * (float(splitContent(content, cmd + " ", index=1)) - 32))
    elif cmd in ["thepenguincommand", "tpc", "thewavecommand", "twc"]: await oneLineCmd(msg, random.choice(("very nice!", "very cool!", ":TiredPuffle:")))
    elif cmd == "daily": await oneLineCmd(msg, f"you earned ${random.randint(0, 1000000)} you can use this command once a day!")
    elif cmd == "reverse": await oneLineCmd(msg, splitContent(content, f'{cmd} ')[1][::-1])
    elif cmd == "imscared": await oneLineCmd(msg, random.choice(("don't be :smiling_imp:", "oh it's ok :)))))))))))))))))", "just don't pay attention of the sounds coming from your attic.....\nit's ok", "it's ok... he's comming :)")))
    elif cmd == "doihavecovid": await oneLineCmd(msg, "yes" if random.random() < .995 else "no")
    elif cmd in ["ship", "boat", "boip"]: await oneLineCmd(msg, "DISCLAIMER: I DO NOT SUPPORT SHIPPING PEOPLE IN ANY WAY, HOWEVER MY MASTER SEEMS TO HAVE OTHER PLANS" if random.random() >= .985 else f'{splitContent(content, ", ")[0].replace("[" + cmd + " ", "")[0:len(splitContent(content, ", ")[0].replace("[" + cmd + " ", "")) // 2]}{splitContent(content, ", ")[1][len(splitContent(content, ", ")[1]) // 2:]}')
    elif cmd == "version": await oneLineCmd(msg, VERSION)
    elif cmd in ["ttc", "thetroycommand"]: await oneLineCmd(msg, random.choice(("meow", "7", "**7**", "*7*", "mo", ":TiredPuffle:")))
    elif cmd == "flush": await oneLineCmd(msg, f"{splitContent(content.lower(), f'{cmd} ')[1]} has been flushed down the toilet :toilet::toilet::toilet::toilet::toilet::toilet::toilet::toilet:")
    elif cmd == "longmessage": await oneLineCmd(msg, "```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````hI```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
    elif cmd in ["wiki", "wikipedia"]: await oneLineCmd(msg, f'https://en.wikipedia.org/wiki/Special:Search?search={content[len(cmd) + 2:].replace(" ", "_")}')
    elif cmd == "commandcount": await oneLineCmd(msg, (len(CMDLIST)))
    elif cmd == "fortnite": await oneLineCmd(msg, "play minecraft instead")
    elif cmd == "slowdown": await oneLineCmd(msg, " **Slow Down** 🐌")

    elif cmd in ["eccmd", "editcustomcmd"]:
        content = await editCustomCmd(msg, content, cmd=cmd)
        CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    elif cmd in ["customcmd", "accmd", "customcommand"]: 
        content = await addCustomCmd(msg, content, cmd=cmd)
        CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    elif cmd in ["removecustomcmd", "delcustomcmd", "dccmd", "rccmd"]: 
        content = await removeCustomCmd(msg, content, cmd=cmd)
        CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    elif cmd == "customcmdlist": await customCmdList(msg, content, cmd=cmd)
    elif cmd in CUSTOMCMDS.keys(): 
        say = CUSTOMCMDS[cmd].replace("{content}", content[len(cmd) + 2:]).replace("{version}", VERSION).replace("{author}", msg.author.mention)
        temp = say.split("{")
        if len(temp) > 1:
            tempCMDSLIST = tuple(x["name"] for x in CMDLIST)
            for line in temp:
                if (cmd := line.split("}")[0].split(" ")[0].strip()) in tempCMDSLIST:
                    foo = line.split("}")[0]
                    mssg = await runCommand(msg, foo, cmd=cmd)
                    temp[temp.index(line)] = mssg.content + line.split("}")[1]
                    await mssg.delete()
        say = "".join(temp)
        content = await oneLineCmd(msg, say)
    elif cmd not in CMDLIST: 
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

    if not content: return
    if testInContent(content, "[delete") or (msg.author.id == 311621977339068418 and msg.channel.id not in (715043261110288415, 658815060646297659)): await msg.delete() #deletes message if requested or myustiak sent it
    if testInContent(content, "[delin "):
        t = splitContent(content, "[delin", index=1).strip()
        try: await asyncio.sleep(int(t))
        except: return await msg.channel.send("NaN")
        await msg.delete()

    if (s := testInContent(content, "[rw", "[reactwith")):
        c = splitContent(content, s, index=1).strip()
        if testInContent(c, ", "):
            c = c.replace(" ", "")
            split = splitContent(c, ",")
            for s in split:
                if s in client.emojis: await msg.add_reaction(discord.utils.get(client.emojis, id=int(s.split(":")[2][:-1])))
                else: await msg.add_reaction(s)
        else:
            e = discord.utils.get(client.emojis, id=int(c.split(":")[2][:-1])) if c in client.emojis else c
            await msg.add_reaction(e)
        
    if msg.channel.id == 427973752647712768 or testInContent(content, "[chkx", "[reactchkx", "[p"):
        await msg.add_reaction(blueCheck)
        await msg.add_reaction(neutral)
        await msg.add_reaction("❌")

    if random.random() >= .9995: 
        if isBot(msg, client): return
        await msg.channel.send(random.choice(("mhm", "interesting", "fascinating", "very cool")))
        
    if content == f'is <@!{client.user.id}> a bot' or content == f'are you a bot <@!{client.user.id}>':
        return await msg.channel.send(f"no {discord.utils.get(client.emojis, name='Watching1')}")

    if f"<@!{client.user.id}>" in content and client.user.id not in playingHangman.keys():
        await msg.channel.send(random.choice((discord.utils.find(lambda e: e.name.lower() == "watching1", client.emojis), discord.utils.find(lambda e: e.name.lower() == "pinged", client.emojis))))
        
    await giveXP(msg)
    await reduceXP(msg)

    if content[0] in PREFIX:

        cmd = getCmd(content)
        WriteToFile = False

        if TICDelete(content): 
            content = content.replace(" --delete", "")
            await msg.delete()

        if testInContent(content, ">>> "):
            WriteToFile = splitContent(content, ">>> ")[1]
            content = content.replace(f">>> {WriteToFile}", "")

        if msg.mention_everyone:
            return await msg.channel.send("NO")

        with open(bannedFilePath, "r") as bannedJ:
            data = json.load(bannedJ)
            if cmd in str(data.get(str(msg.author.id))):
                return await msg.channel.send(f"You cannot use {cmd}")

        #ongoing events			
        if cmd == "guessinggame":
            c = splitContent(content, cmd)[1]
            if testInContent(content, "--bet"):
                Bet = True
                c = c.replace(" --bet", "")
            else: Bet = False
            low, high, lives = 1, 100, 5
            if len(c) > 0 and not Bet:
                c = c.split(" ")
                c.pop(0)
                low = int(c[0])
                high = int(c[1])
                if len(c) >= 3: lives = int(c[2])
            ans = random.randint(low, high)
            playingGuessingGame[msg.author.id] = {"ans": ans, "lives": lives, "startLives": lives, "bet": Bet}
            return await msg.channel.send("guess")

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
        elif cmd == "stop":
            if TICDelete(content): await msg.message.delete()
            await stop()
        else: 
            content = await runCommand(msg, content, cmd)
            if WriteToFile:
                await writeToFile(msg, content.content, WriteToFile)
                await content.delete()

    if playingGuessingGame.get(msg.author.id):
        c = msg.content
        ans = playingGuessingGame[msg.author.id]["ans"]
        lives = playingGuessingGame[msg.author.id]["lives"]
        startLives = playingGuessingGame[msg.author.id]["startLives"]
        Bet = playingGuessingGame[msg.author.id]["bet"]
        if c in ["stop", "giveup", "cancel"]:
            await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(100, 0, 0)))
            del playingGuessingGame[msg.author.id]
        elif isInt(c):
            lives -= 1
            if lives <= 0:
                if int(content) == ans: await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} ITS A DRAW', color=discord.Color.from_rgb(155, 155, 155)))
                else: 
                    say = f"YOU LOSE\nTHE ANSWER WAS {ans}" if not Bet else f'YOU LOSE\nTHE ANSWER WAS {ans}\nYOU LOSE {(int(ans) // startLives)}'
                    await msg.channel.send(embed=discord.Embed(title=say, color=discord.Color.from_rgb(255, 0, 0)))
                del playingGuessingGame[msg.author.id]
                if Bet: await addMoney(msg.author, -(int(ans) // startLives))
                return str(ans)
            elif int(content) == ans:
                say = f"YOU WIN\nWITH {lives} LIVES LEFT" if not Bet else f'YOU WIN\nWITH {lives} LIVES LEFT\nYou earned {(int(ans) // startLives)}'
                await msg.channel.send(embed=discord.Embed(title=say, color=discord.Color.from_rgb(0, 255, 0)))
                del playingGuessingGame[msg.author.id]
                if Bet: await addMoney(msg.author, (int(ans) // startLives))
                return str(ans)
            await msg.channel.send(f"{msg.author.mention} too high" if int(c) > ans else f"{msg.author.mention} too low")
        playingGuessingGame[msg.author.id]["lives"] = lives
        await msg.channel.send(f"guess\nyou have {lives} lives left")

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

@client.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        role = discord.utils.get(member.guild.roles, name="vc")
        await member.add_roles(role)
    elif before.channel and not after.channel:
        role = discord.utils.get(member.guild.roles, name="vc")
        await member.remove_roles(role)

client.run(token)