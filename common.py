import discord
from discord.ext import commands
import time, datetime
import random
import string
import asyncio
import json
import tracemalloc
import requests
import bs4 as bs
import os
import math
import statistics
import re
import sys
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont, ImageChops

DELETE = "--delete"
VERSION = "4.11.2"
Stop = False

playingGuessingGame = {}
playingHangman = {}
playingDB = []

#CONSTS
PREFIX = "]"
UPTIME = time.time()
fakePrefix = PREFIX
token = "NjQxNzk1NjU2Mzc3MTcyMDAw.XcNk8g.HEvnaXjuXFQhN1iilaaffbiPcoo"
HPKEY = "544fcd57-1cb1-4d8a-8613-c156d7e8f4ed"
DISEXT = "../disbot_ext"
BASICINFO = {"level": 1, "xp": 0, "required": 1000, "lastTalked": 0, "message": '{author} you have leveled up to level {level}, very cool'}
mballresponseFilePath = f"{DISEXT}/mballresponse.txt"
levelingDataFilePath = f"{DISEXT}/levelingData.json"
commandusageFilePath = f"{DISEXT}/commandusage.json"
customcmdsFilePath = f'{DISEXT}/customcmds.json'
bannedFilePath = f"{DISEXT}/banned.json"
timersPath = f"{DISEXT}/timers.json"
moneyDataFilePath = f'{DISEXT}/moneyData.json'
itemDataFilePath = f'{DISEXT}/itemsData.json'
botModsFilePath = f'{DISEXT}/botMods.txt'
itemsFilePath = f'items.json'
pingResponseFilePath = f'{DISEXT}/pingresponse.json'
EUROID = 334538784043696130
client = commands.Bot(command_prefix=fakePrefix)

tracemalloc.start()

async def returnMessage(msg, content, author=client.user):
    msg.content = content
    msg.author = author
    return msg

def reloadBOTMODS():
    global BOTMODS
    with open(botModsFilePath, "r") as f:
        BOTMODS = f.read().split("\n")
    return BOTMODS

async def saveImg(filename, url):
    with open(filename, 'wb') as i:
        response = requests.get(url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            i.write(block)

async def imgInChat(msg, limit=20):
    async for mssg in msg.channel.history(limit=limit):
        if mssg.embeds:
            if mssg.embeds[0].image:
                att = mssg.embeds[0].image
                url = att.url
                filename = url.split("/")[-1]
                break
            if mssg.embeds[0].thumbnail:
                att = mssg.embeds[0].thumbnail
                url = att.url
                filename = url.split("/")[-1]
                break
        if mssg.attachments:
            att = mssg.attachments[0]
            filename = att.filename
            url = att.url
            break
    else: return "USER"
    return att, filename, url

async def getImg(msg, user=None):
    if "https://" in msg.content:
        att = None
        filename = "UNKNOWN.png"
        url = msg.content.split(" ")[-1]
    elif msg.attachments:
        att = msg.attachments[0]
        filename = att.filename
        url = att.url
    else: 
        tup = await imgInChat(msg)
        if tup != "USER":
            att, filename, url = tup
        elif tup == "USER":
            att = msg.author.avatar if not user else user.avatar
            filename = "UNKNOWN.png"
            url = msg.author.avatar_url if not user else user.avatar_url
        else:
            return await msg.channel.send("no img provided")
    return att, filename, url

async def reloadCMDSLIST():
    with open("cmds.json", "r") as cmdsJson:
        data = json.load(cmdsJson)
        with open(customcmdsFilePath, "r") as customJson:
            foo = json.load(customJson)
            for cat in data:
                if cat["cat"] == "CUSTOM":
                    cat["cmds"] = foo
        CATS = {cat["cat"]: cat["cmds"] for cat in data}
        CMDLIST = tuple(cmd for _ in CATS.values() for cmd in _) #gets a list of commands
        CUSTOMCMDS = {cmd["name"]: cmd["desc"] for cmd in CATS["CUSTOM"]}
    return CATS, CMDLIST, CUSTOMCMDS

def isBot(msg, client)->bool:
    return msg.author == client.user or msg.author.bot

async def embedToReadableDict(msg, embed):
    d = embed.to_dict()
    msg.content = d["title"] + "\n"
    for k in d.keys():
        if k == "color" or k == "type": continue
        if k == "fields":
            for field in d[k]:
                msg.content += f'{field["name"]}: {field["value"]}\n'
    return msg

async def writeToFile(msg, content, F):
    if "." in F: 
        ext = F.split(".")[1]
        F = F.replace(f".{ext}", "")
    else: ext = "txt"
    with open(f"{F}.{ext}", "w") as f:
        f.write(content)
    with open(f"{F}.{ext}", "rb") as f:
        await msg.channel.send(file=discord.File(f, f"{F}.{ext}"))
    os.remove(f'{F}.{ext}')

async def removeFromList(l, *args):
    for arg in args: l.remove(arg)

async def formatSeconds(t, layer="seconds", stopAt=None, rec=0):
    cases = {"seconds": ("minutes", 60),
             "minutes": ("hours", 60), 
             "hours": ("days", 24), 
             "days": ("weeks", 7)
             }
    if layer == "weeks" or layer == stopAt: return t, layer
    if t >= cases[layer][1] or (layer != stopAt and stopAt):
        t /= cases[layer][1]
        t, layer = await formatSeconds(t, layer=cases[layer][0], stopAt=stopAt, rec=rec + 1)
    return t, layer

async def formatLevelMessage(msg, message, level): #gives the levelmessage with the keywords replaced
    if "{emote}" in message:
        new = [x if x != "{emote}" else str(random.choice(client.emojis)) for x in message.split(" ")]
        message = " ".join(new)
    return message.replace("{author}", msg.author.mention).replace("{level}", str(level)).replace("{channel}", msg.channel.mention)

async def formatDateTime(createdAt : datetime.datetime)->str:
    return f'{createdAt.month}/{createdAt.day}/{createdAt.year}\nat {createdAt.hour}:{createdAt.minute}:{createdAt.second}'

async def getUserInContent(msg : discord.Message, c : str, cmd : str)->discord.User: #gets user by id, name, etc
    c = str(c.split(cmd)[1].strip())
    c = c.replace("!", "")[2:-1] if "<@" in c else c
    if not c: c = str(msg.author.id)
    user = findMember(c, msg)
    user = msg.author if not user else user
    return user

async def giveXP(msg : discord.Message)->None:
    if isBot(msg, client): return
    with open(levelingDataFilePath, "r+") as f:
        data = json.load(f)
        userInfo = data.get(str(msg.author.id))
        if userInfo:
            lastTalked = int(userInfo["lastTalked"])
            if time.time() - lastTalked >= 60:
                level = userInfo["level"]
                xp = userInfo["xp"]
                xp += random.randint(15, 100)
                lastTalked = time.time()
                required = userInfo["required"]
                levelUpMessage = userInfo.get("message")
                if not levelUpMessage: levelUpMessage = '{author} you have leveled up to level {level}, very cool'
                if xp >= required:
                    with open(moneyDataFilePath, "r+") as j:		
                        moneyData = json.load(j)
                        if moneyData.get(str(msg.author.id)):
                            moneyData[str(msg.author.id)] += int((level + 1) * 2)
                        else: moneyData[str(msg.author.id)] = int((level + 1) * 2)
                        clearFile(j)
                        json.dump(moneyData, j)
                    level += 1; xp //= 2 #gives level; reduces xp
                    disp = await formatLevelMessage(msg, levelUpMessage, level)
                    if disp not in ["none", "None", "null", "Null"]:
                        await msg.channel.send(disp)
                required = round((1000 * level) * 1.1)
                userInfo = {"level": level, "xp": xp, "required": required, "lastTalked": lastTalked, "message": levelUpMessage}
            data[str(msg.author.id)] = userInfo
        else:
            data[str(msg.author.id)] = BASICINFO
            data[str(msg.author.id)]["lastTalked"] = time.time()
        clearFile(f)
        json.dump(data, f)

async def reduceXP(msg : discord.Message)->None:
    if isBot(msg, client): return
    with open(levelingDataFilePath, "r+") as f:
        data = json.load(f)
        for user in data.keys():
            if time.time() - data[user]["lastTalked"] >= 1209600:
                if data[user]["xp"] > 1:
                    data[user]["xp"] -= random.randint(0, 1)
                if data[user]["xp"] <= (data[user]["level"] * 1000) // 2 and data[user]["level"] > 0:
                    data[user]["level"] -= 1
                    data[user]["xp"] = (data[user]["level"] * 1000) - 1
        clearFile(f)
        json.dump(data, f)

def testInContent(content : str, *testfor)->str:
    for x in testfor:
        if x.lower() in content.lower():
            return x
    return ""

def TICDelete(content : str)->bool:
    return DELETE in content

def getCmd(content : str)->str:
    return content.split(" ")[0][1:]				

def splitContent(content : str, *split, index=None, func=None)->str:
    for x in split:
        if x in content: #this is an IF STATEMENT, don't think it's a for loop
            ret = content.split(x)
            if func and index:
                ret = func(content.split(x)[index])
            elif func: ret = func(x)
            elif index: ret = content.split(x)[index]
            return ret
    return ""

def isInt(testee : str)->bool:
    try: 
        int(testee)
        return True
    except:	return False
    
def userHasRole(msg : discord.Message, *roles)->bool:
    return True if discord.utils.find(lambda r: r.name in roles, msg.author.roles) else False

def findMember(c : str, msg : discord.Message)->discord.Member:
    return discord.utils.find(lambda m: str(m.id) == c or str(m.display_name.split("#")[0].lower()) == c.lower() or m.name.lower() == c.lower(), msg.guild.members)

def clearFile(f)->None:
    f.seek(0)
    f.truncate()

async def oneLineCmd(msg : discord.Message, say : str, delete=True, sendMsg=True, cmd=None)->discord.Message:
    if sendMsg: return await msg.channel.send(say)
    else:
        msg.content = say
        return msg

async def addMoney(member, amnt):
    with open(moneyDataFilePath, "r+") as j:
        data = json.load(j)
        if data.get(str(member.id)):
            data[str(member.id)] += amnt
        else: data[str(member.id)] = amnt
        clearFile(j)
        json.dump(data, j)
