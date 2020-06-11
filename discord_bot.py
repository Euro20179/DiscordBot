from common import *
from cmds import *

async def runCommand(msg, content, cmd, layer=1):
    global CUSTOMCMDS, CATS, CMDLIST
    DOFIRST = f"--{layer} "
    if DOFIRST in content:
        c = await runCommand(msg, content.split(DOFIRST)[1], splitContent(content, DOFIRST, index=1).split(" ")[0][1:], layer=layer+1)
        content = f'{content.split(f" {DOFIRST}")[0]} {c.content}'
        await c.delete()

    with open(commandusageFilePath, "r+") as j:
        data = json.load(j)
        try: data[cmd] += 1
        except: data[cmd] = 1
        clearFile(j)
        json.dump(data, j)
        
    if cmd == "timeit":
        start = time.time()
        await runCommand(msg, content.replace('[timeit ', ""), splitContent(content, "timeit ", index=1).split(" ")[0][1:])
        return await msg.channel.send(time.time() - start)

    elif cmd == "ENDPLS" and msg.author.id == EUROID:
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

    elif cmd == "BAN" and msg.author.id == EUROID:
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

    elif cmd == "UNBAN" and msg.author.id == EUROID:
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

    elif cmd == "timers": content = await timers(msg, content)
    elif cmd == "echo": content = await echo(msg, content)
    elif cmd == "ping": content = await ping(msg, content)
    elif cmd == "help": content = await hlp(msg, content)
    elif cmd in ["commandusage", "cmduse", "cmdusage", "commanduse"]: content = await cmdUsage(msg, content, cmd=cmd)
    elif cmd in ["findans", "equation", "result", "eval", "calc"]: content = await calc(msg, content, cmd=cmd)
    elif cmd == "iq": content = await iq(msg, content)
    elif cmd == "shrug": content = await shrug(msg, content)
    elif cmd in ["level", "rank", "lvl"]: content = await level(msg, content, cmd=cmd)
    elif cmd in ["top", "leaderboard", "levels", "lb"]: content = await leaderboard(msg, content)
    elif cmd in ["magicball", "8ball", "7ball"]: content = await magicBall(msg, content, cmd=cmd)
    elif cmd == "spam": content = await spamCmd(msg, content)
    elif cmd in ["randomface","randface", "rface"]: content = await randomFace(msg, content, cmd=cmd)
    elif cmd in ["ttc", "thetroycommand"]: content = await oneLineCmd(msg, random.choice(("meow", "7", "**7**", "*7*", "mo", ":TiredPuffle:")))
    elif cmd in ["thepenguincommand", "tpc", "thewavecommand", "twc"]: content = await oneLineCmd(msg, random.choice(("very nice!", "very cool!", ":TiredPuffle:")))
    elif cmd in ["mmoney", "mymoney", "money", "bal"]: content = await mmoney(msg, content, cmd)
    elif cmd in ["ucodechar", "unicodechar"]: content = await unicodeChar(msg, content, cmd=cmd)
    elif cmd == "serveremote": content = await serverEmote(msg, content)
    elif cmd == "doesnothing": content = await writeRoles(msg, content)
    elif cmd == "spacer": content = await spacer(msg, content)
    elif cmd == "version": content = await oneLineCmd(msg, VERSION)
    elif cmd in ["upperlower", "ul"]: content = await upperLower(msg, content, cmd=cmd)
    elif cmd == "longmessage": content = await oneLineCmd(msg, "```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````hI```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
    elif cmd in ["rps", "rockpaperscissors"]: await startRPS(msg, content, cmd=cmd)
    elif cmd == "flush": content = await oneLineCmd(msg, f"{splitContent(content.lower(), f'{cmd} ')[1]} has been flushed down the toilet :toilet::toilet::toilet::toilet::toilet::toilet::toilet::toilet:")
    elif cmd in ["complexmessage", "message"]: content = await complexMessage(msg, content, cmd=cmd)
    elif cmd == "sanity": content = await sanity(msg, content)
    elif cmd == "coin": content = await coin(msg, content)
    elif cmd == "roleinfo": content = await roleInfo(msg, content)
    elif cmd == "rand": content = await rand(msg, content)
    elif cmd == "rolecount": content = await roleCount(msg, content)
    elif cmd in ["ship", "boat", "boip"]: content = await oneLineCmd(msg, "DISCLAIMER: I DO NOT SUPPORT SHIPPING PEOPLE IN ANY WAY, HOWEVER MY MASTER SEEMS TO HAVE OTHER PLANS" if random.random() >= .985 else f'{splitContent(content, ", ")[0].replace("[" + cmd + " ", "")[0:len(splitContent(content, ", ")[0].replace("[" + cmd + " ", "")) // 2]}{splitContent(content, ", ")[1][len(splitContent(content, ", ")[1]) // 2:]}')
    elif cmd in ["comproles", "compareroles"]: content = await compareRoles(msg, content, cmd=cmd)
    elif cmd == "family": content = await family(msg, content)
    elif cmd == "mballreply": content = await mballreply(msg, content)
    elif cmd == "8brdel": content = await mballDel(msg, content)			
    elif cmd == "count": content = await count(msg, content)
    elif cmd == "choose": content = await choose(msg, content)
    elif cmd in ["mballreplylist", "8ballreplylist", "8breplylist", "8brlist"]: content = await mball(msg, content, cmd=cmd)
    elif cmd == "reverse": content = await oneLineCmd(msg, splitContent(content, f'{cmd} ')[1][::-1])
    elif cmd in ["piglatin", "igpayatinlay"]: content = await pigLatin(msg, content, cmd=cmd)
    elif cmd == "mostroles": content = await mostRoles(msg, content)
    elif cmd == "imscared": content = await oneLineCmd(msg, random.choice(("don't be :smiling_imp:", "oh it's ok :)))))))))))))))))", "just don't pay attention of the sounds coming from your attic.....\nit's ok", "it's ok... he's comming :)")))
    elif cmd == "clear": content = await clear(msg, content)
    elif cmd == "color": content = await color(msg, content)
    elif cmd == "servericon": content = await serverIcon(msg, content)
    elif cmd in ["cc", "channelcreated", "channelinfo", "ci"]: content = await channelInfo(msg, content, cmd=cmd)
    elif cmd == "changes": content = await changes(msg, content)					
    elif cmd in ["wiki", "wikipedia"]: content = await oneLineCmd(msg, f'https://en.wikipedia.org/wiki/Special:Search?search={content[len(cmd) + 2:].replace(" ", "_")}')
    elif cmd == "commandcount": content = await oneLineCmd(msg, (len(CMDLIST)))
    elif cmd in ["hex", "bin", "oct"]: content = await hexBinOct(msg, content, cmd=cmd)
    elif cmd == "tof": content = await oneLineCmd(msg, 9 / 5 * float(splitContent(content, cmd + " ", index=1)) + 32)
    elif cmd == "toc": content = await oneLineCmd(msg, 5 / 9 * (float(splitContent(content, cmd + " ", index=1)) - 32))
    elif cmd == "response": content = await response(msg, content)
    elif cmd in ["stopwatch", "timer"]: content = await stopwatch(msg, content, cmd=cmd)
    elif cmd == "lvlmsg": content = await levelMessage(msg, content)
    elif cmd == "emoteinfo": content = await emoteInfo(msg, content)
    elif cmd == "avatar": content = await msg.channel.send((await getUserInContent(msg, content, cmd)).avatar_url)
    elif cmd == "slowdown": content = await oneLineCmd(msg, " **Slow Down** 🐌")
    elif cmd == "fetchuser": content = await msg.channel.send((await client.fetch_user(int(splitContent(content, f'{cmd} ', index=1)))).name)
    elif cmd == "clearinvites": content = await ridInvites(msg, content)
    elif cmd == "typefor": content = await typeFor(msg, content)
    elif cmd == "hangman": content = await hangman(msg, content)
    elif cmd == "sendblank": content = await sendBlank(msg, content)
    elif cmd == "daily": content = await oneLineCmd(msg, f"you earned ${random.randint(0, 1000000)} you can use this command once a day!")
    elif cmd == "serverinfo": content = await serverInfo(msg, content)
    elif cmd == "pokemon": content = await pokemon(msg, content)
    elif cmd == "userinfo": content = await userInfo(msg, content)
    elif cmd in ["msginfo", "messageinfo"]: content = await messageInfo(msg, content, cmd=cmd)
    elif cmd == "fetchrole": content = await fetchRole(msg, content)
    elif cmd == "categoryinfo": content = await categoryInfo(msg, content)
    elif cmd in ["alphabet", "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"]: content = await alphabet(msg, content, cmd=cmd)
    elif cmd == "spamstop": content = await spamStop(msg, content)
    elif cmd == "doihavecovid": content = await oneLineCmd(msg, "yes" if random.random() < .995 else "no")
    elif cmd == "covid": content = await covid(msg, content)
    elif cmd == "hypixelpc": content = await hypixelPlayerCount(msg, content)
    elif cmd == "hasrole": content = await whoHasRole(msg, content)
    elif cmd == "customcmd": 
        content = await addCustomCmd(msg, content)
        CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    elif cmd in ["removecustomcmd", "delcustomcmd", "dccmd", "rccmd"]: 
        content = await removeCustomCmd(msg, content, cmd=cmd)
        CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    elif cmd in ["db", "deathbattle"]: content = await INIT_deathBattle(msg, content, cmd=cmd)
    elif cmd == "shop": content = await shop(msg, content)
    elif cmd in ["buyitem", "buy"]: content = await buyItem(msg, content, cmd=cmd)
    elif cmd in ["inv", "inventory"]: content = await inventory(msg, content, cmd=cmd)
    elif cmd == "customcmdlist": 
        CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
        content = await oneLineCmd(msg, "\n".join([f'{x}: {y}' for x, y in CUSTOMCMDS.items()]))
    elif cmd in CUSTOMCMDS.keys(): content = await oneLineCmd(msg, CUSTOMCMDS[cmd])
    elif cmd not in CMDLIST: 
        with open(commandusageFilePath, "r+") as j:
            data = json.load(j)
            del data[cmd]
            clearFile(j)
            json.dump(data, j)
        content = await msg.channel.send(f'{cmd} {random.choice(("is not a thing", "does not exist"))}')
    return content

@client.event
async def on_ready():
    global blueCheck, neutral, CATS, CMDLIST, CUSTOMCMDS
    await client.change_presence(activity=discord.Game(f'version: {VERSION}'))
    blueCheck = discord.utils.get(client.emojis, name="Blue_check")
    neutral = discord.utils.get(client.emojis, name="neutral")
    CATS, CMDLIST, CUSTOMCMDS = await reloadCMDSLIST()
    print(f"ONLINE\nversion: {VERSION}")

@client.event
async def on_message(msg):
    global Stop, playingGuessingGame
    global blueCheck, neutral

    content = msg.content

    if not content: return
    if testInContent(content, "---delete") or (msg.author.id == 311621977339068418 and msg.channel.id not in (715043261110288415, 658815060646297659)): await msg.delete() #deletes message if requested or myustiak sent it
    if testInContent(content, "--delin "):
        t = splitContent(content, "--delin", index=1).strip()
        try: await asyncio.sleep(int(t))
        except: return await msg.channel.send("NaN")
        await msg.delete()

    if (s := testInContent(content, "--rw", "--reactwith")):
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
        
    if msg.channel.id == 427973752647712768 or testInContent(content, "--chkx", "--reactchkx", "--p"):
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

        if msg.mention_everyone:
            return await msg.channel.send("NO")

        with open(bannedFilePath, "r") as bannedJ:
            data = json.load(bannedJ)
            if cmd in str(data.get(str(msg.author.id))):
                return await msg.channel.send(f"You cannot use {cmd}")

        #ongoing events			
        if cmd == "guessinggame":
            c = splitContent(content, cmd)[1]
            low, high, lives = 1, 100, 5
            if len(c) > 0:
                c = c.split(" ")
                c.pop(0)
                low = int(c[0])
                high = int(c[1])
                if len(c) >= 3: lives = int(c[2])
            ans = random.randint(low, high)
            playingGuessingGame[msg.author.id] = {"ans": ans, "lives": lives}
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
        else: await runCommand(msg, content, cmd)

    if playingGuessingGame.get(msg.author.id):
        c = msg.content
        ans = playingGuessingGame[msg.author.id]["ans"]
        lives = playingGuessingGame[msg.author.id]["lives"]
        if c in ["stop", "giveup", "cancel"]:
            await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(100, 0, 0)))
            del playingGuessingGame[msg.author.id]
        elif isInt(c):
            lives -= 1
            if lives <= 0:
                if int(content) == ans: await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} ITS A DRAW', color=discord.Color.from_rgb(155, 155, 155)))
                else: await msg.channel.send(embed=discord.Embed(title=f'{msg.author.display_name} YOU LOSE\nTHE ANSWER WAS {ans}', color=discord.Color.from_rgb(255, 0, 0)))
                del playingGuessingGame[msg.author.id]
            elif int(content) == ans:
                await msg.channel.send(embed=discord.Embed(title=f"{msg.author.display_name} YOU WIN\nWITH {lives} LIVES LEFT", color=discord.Color.from_rgb(0, 255, 0)))
                del playingGuessingGame[msg.author.id]
                return ""
            await msg.channel.send("too high" if int(c) > ans else "too low")
        else: await msg.channel.send("NaN")
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