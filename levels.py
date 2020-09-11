from common import *
from gamesandmoney import mostmoney

command.setCategory("levels", "anything that has to do with leveling")

@command
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
    await UserInfo.registerUser(user.id)
    await RAMUserInfo[user.id].dumpLevelInfo()
    userData = RAMUserInfo[user.id]
    with open(levelingDataFilePath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        users = [(discord.utils.get(msg.guild.members, id=int(user.id)).id, int(data[userr]["level"])) for userr in data.keys()]
        users.sort(key=lambda x: x[1], reverse=True)
    level = userData.level
    xp = userData.xp
    required = userData.required
    message = userData.levelUpMessage
    pos = users.index((user.id, level)) + 1
    embed = discord.Embed(title=user.display_name, color=user.color)
    embed.add_field(name="level", value=str(level))
    embed.add_field(name="xp", value=str(xp))
    embed.add_field(name="required", value=str(required))
    embed.add_field(name="rank #", value=pos)
    embed.add_field(name="xp needed", value=required - xp)
    time, layer = await formatSeconds(((required - xp) / 57.5), layer="minutes")
    embed.add_field(name="approx time", value=f'{round(time, 5)} {layer}') #TODO format this
    embed.add_field(name="level up mesage", value=str(Content(message, removeCmd=False).formatMessage(msg, kwargs={"{level}": level + 1, "{xp}": xp}, removeCmd=False, ret=True)), inline=False)
    return await returnMsg(msg, embed=embed)

@command
async def leaderboard(msg, content, cmd="top"):
    """
    the leaderboard of the highest leveled people
    optional params:
        [top]: the amount of people to show
        [m]: alias to mostmoney
    options:
        --html: generates an html file instead of an embed (always shows everyone)
        --money: alias to mostmoney
        --m: alias to mostmoney
    aliases:
        levels
        top
        leaderboard
        lb
    added: "5/23/2020
    """
    content = Content(content)
    if content.testOps("--money", "--m", "--bal") or content.string.strip() == "m":
        return await mostmoney(msg, content, cmd="mostmoney")
    for user in RAMUserInfo.values():
        if type(user) is str: continue
        await user.dumpLevelInfo()
    if content @ "--raw":
        with open(levelingDataFilePath, "rb") as f:
            return await returnMsg(msg, file=discord.File(f, levelingDataFilePath))
    top = 10
    if str(content):
        try: top = int(content)
        except: return await returnMsg(msg, "NaN")
    with open(levelingDataFilePath, "r", encoding="utf-8-sig") as f:
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
                html.write("<html>\n<head>\n<meta charset='utf-8'><style>p:active{font-size:2em;}\np {border-bottom: 1px dashed red; color:white;}</style></head><body style='font-family:arial;font-size:20px;background-color:#333'>")
                for n, user in enumerate(users):
                    if user[0]:
                        time, layer = await formatSeconds(((user[3] - user[2]) / 57.5), layer="minutes")
                        html.write(f'<p>{n + 1}: User: {user[0].name} <br />Level: {user[1]} <br /> Xp: {user[2]} <br /> Required: {user[3]} <br /> Xp Needed: {user[3] - user[2]} <br /> Approx time: {time} {layer}')
                html.write("</body>\n</html>")
            with open("top.html", "rb") as html:
                msg = await returnMsg(msg, file=discord.File(html, "top.html"))
            os.remove("top.html")
            return msg

@command
async def levelMessage(msg, content, cmd="lvlmsg"):
    """
    when you level up it will say what you give it here
    required params:
        <level message>: the message to set the lvlmsg to
    options:
        --see/--get/--s/--g: shows what will happen when you level up
        --f/--y: automatically agrees to change it
    FORMATS AND {level}, {xp}
    aliases:
        lvlmsg
        levelmessage
        levelupmessage
        levelupmsg
        lvlupmsg
    added: 5/29/2020
    """
    changeTo = Content(content)
    unTampered = changeTo.string
    changeTo = changeTo.calcOps(rep=True)
    yn = changeTo @ "--y"
    if yn: 
        unTampered = unTampered.replace("--y", "")
    userData = RAMUserInfo[msg.author.id]
    if changeTo.testOps("--see", "--get", "--s", "--g"):
        content = Content(userData.levelUpMessage, removeCmd=False)
        content.formatMessage(msg, {"{level}": userData.level + 1, "{xp}": userData.xp}, removeCmd=False)
        return await returnMsg(msg, str(content))
    if changeTo.testOps("--dontsee"):
        return await returnMsg(msg, "uh, ok then")
    if not yn:
        await msg.channel.send("type y to change message, type n to cancel")
        try: yn = (await client.wait_for('message', check=lambda message: message.author == msg.author, timeout=60.0)).content.lower()
        except asyncio.TimeoutError: yn = "n"
    if yn in ("yes", "y") or yn is True:
        userData.levelUpMessage = str(unTampered)
        return await returnMsg(msg, f"changed to {unTampered}")
    return await returnMsg(msg, "CANCELLED")