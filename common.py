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
import os, shutil
import math
import statistics
import re
import sys
import youtube_dl
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont, ImageChops

DELETE = "--delete"
VERSION = "5.0-rc15"
Stop = False

playingGuessingGame = {}
playingHangman = {}
playingDB = []

#CONSTS
PREFIX = "["
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
botModsFilePath = f'{DISEXT}/botMods.json'
itemsFilePath = f'items.json'
pingResponseFilePath = f'{DISEXT}/pingresponse.json'
emoteUsageFilePath = f'{DISEXT}/emoteusage.json'
queuePath = "./queue"
EUROID = 334538784043696130
client = commands.Bot(command_prefix=fakePrefix)

tracemalloc.start()

def reloadBOTMODS():
    global BOTMODS
    with open(botModsFilePath, "r") as f:
        BOTMODS = json.load(f)
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
        if mssg.attachments:
            att = mssg.attachments[0]
            filename = att.filename
            url = att.url
            break
    else: return "USER"
    return att, filename, url

async def getImg(msg, user=None, NotFromChat=False):
    if "https://" in msg.content:
        att = None
        filename = "UNKNOWN.png"
        url = msg.content.split(" ")[-1]
    elif msg.attachments:
        att = msg.attachments[0]
        filename = att.filename
        url = att.url
    elif not NotFromChat: 
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
    msg.content = str(d.get("title")) + "\n"
    for k in d.keys():
        if k == "type": continue
        if k == "fields":
            for field in d[k]:
                msg.content += f'{field["name"]}: {field["value"]}\n'
        if k == "image":
            msg.content += f'{d[k]["url"]}\n'
        if k == "color":
            msg.content += f'Color: {d[k]}\n'
    msg.content = discord.utils.escape_mentions(msg.content)
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
        authorId = str(msg.author.id)
        userInfo = data.get(authorId)
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
                        give = int((level + 1) * 2)
                        if moneyData.get(authorId):
                            moneyData[authorId] += give
                        else: moneyData[authorId] = give
                        clearFile(j)
                        json.dump(moneyData, j)
                    level += 1; xp //= 2 #gives level; reduces xp
                    disp = Content(levelUpMessage, removeCmd=False)
                    disp.formatMessage(msg, {"{level}": level, "{xp}": xp}, removeCmd=False)
                    disp = disp.string
                    if disp not in ["none", "None", "null", "Null"]:
                        await msg.channel.send(disp)
                required = round((1000 * level) * 1.1)
                userInfo = {"level": level, "xp": xp, "required": required, "lastTalked": lastTalked, "message": levelUpMessage}
            else: return
            data[authorId] = userInfo
        else:
            data[authorId] = BASICINFO
            data[authorId]["lastTalked"] = time.time()
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

class Content:
    def __init__(self, string, removeCmd=True):
        if removeCmd:
            split = string.split(" ")
            self.string = " ".join(split[1:])
            self.cmd = split[0]
        else: self.string = string
        self._i = -1
        self.ops_ = []
        self.opOps = []

    def calcOps(self):
        """
        calculates -- options without yielding
        """
        if not self.split(" ") or ("--" not in self and "—" not in self): return []
        for word in reversed(self.split(" ")):
            if "--" in word or "—" in word:
                self.ops_.append(word)
                foo = self.string
                self.replace(f' {word}', "")
                if foo == self.string:
                    self.replace(word, "")

    def split(self, splitBy, pastIndex=None, key=None):
        split = self.string.split(splitBy)
        if key:
            for n, s in enumerate(split):
                transformation = key(s)
                if transformation or not isinstance(transformation, bool):
                    split[n] = transformation
                else: 
                    if not transformation: split.pop(n)
        return split if not pastIndex else splitBy.join(split[pastIndex:])

    def replace(self, string, repWith, ret=False):
        if not ret: self.string = self.string.replace(string, repWith)
        else: return self.string.replace(string, repWith)
    
    def strip(self, other=None):
        return self.string.strip(other) if other else self.string.strip()

    def lower(self):
        return self.string.lower()
    
    def testOps(self, *ops):
        if not self.ops_: self.calcOps()
        for op in ops:
            if op in self.opOps or op in self.ops_:
                return True
        return False
    
    def ops(self):
        self.calcOps()
        for op in self.ops_:
            yield op

    def opsWithParams(self, paramcount : dict =None):
        """
        paramcount could be {'param': arg_num}
        or {'param': (index, split)}
        """
        l = self.split(" ")
        if not l[0]: return [(None, None)]
        for n, word in enumerate(l):
            if not word: continue
            if "-" == word[0] and word[1] != "-":
                if paramcount and word.strip("-") in paramcount.keys():
                    paramCount = paramcount.get(word.strip("-"))
                    if paramCount:
                        if isinstance(paramCount, tuple):
                            index = paramCount[0] if paramCount[0] else 1
                            splitBy = paramCount[1]
                            arg = " ".join(l[n + 1:]).split(splitBy)
                            self.opOps.append(word)
                            self.replace(f'{word} {splitBy.join(arg)}', "")
                            yield (word, arg[index].strip()) if not isinstance(index, slice) else (word, arg[index])
                        else:
                            self.opOps.append(word)
                            arg = l[l.index(word) + 1: l.index(word) + paramCount + 1]
                            self.replace(f'{word} {" ".join(arg)}', "")
                            yield (word, arg)
                else:
                    try:
                        self.opOps.append(word)
                        self.replace(f'{word} {"".join(l[l.index(word) + 1])}', "")
                        yield (word, "".join(l[l.index(word) + 1]))
                    except Exception as e:
                        print(e)
                        self.opOps.append(word)
                        self.replace(word, "")
                        yield(word, None)

    def getUser(self, msg, index=None, content=None):
        """
        index is the index where the user should be when content is split by spaces
        """
        if index:
            try: c = str(self.split(" ")[index].strip())
            except: return msg.author
        else:
            try: c = str(content)
            except: return msg.author
        c = c.replace("!", "")[2:-1] if "<@" in c else c
        if not c: c = str(msg.author.id)
        user = discord.utils.find(lambda m: str(m.id) == c or str(m.display_name.split("#")[0].lower()) == c.lower() or m.name.lower() == c.lower(), msg.guild.members)
        return user if user else msg.author

    def toSet(self, split=" ", pastIndex=None, key=None):
        """
        returns a set split by split
        """
        return set(self.split(" ", pastIndex=pastIndex, key=key))

    def suitibleForEval(self):
        return False if self.toSet() & {"help(", "quit()", "exit()", "os.", "token", "input(", "sys.", "__import__('os')", '__import__("os")',} else True
    
    def formatMessage(self, msg, kwargs=None, removeCmd=True):
        if "{emote}" in self:
            new = [x if x.strip() != "{emote}" else str(random.choice(msg.guild.emojis)) for x in self.split(" ")]
            self.string = " ".join(new)
        self.replace("{content}", str(Content(msg.content, removeCmd=removeCmd)))
        self.replace("{version}", VERSION)
        self.replace("{author}", msg.author.mention)
        self.replace("{uptime}", str(time.time() - UPTIME))
        self.replace("{channel}", msg.channel.mention)
        self.replace("{fhalf}", self[0:(len(self) - 7) // 2])
        if kwargs:
            for k, i in kwargs.items():
                print(self)
                self.replace(str(k), str(i))

    def __len__(self):
        return len(self.string)

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __add__(self, other):
        return self.string + other

    def __contains__(self, other):
        return other in self.string

    def __matmul__(self, other):
        if not self.ops_: self.calcOps()
        return other in self.ops_

    def __getitem__(self, other):
        if isinstance(other, slice):
            start, stop, step = other.indices(len(self))
            return self.string[start:stop:step]
        try:
            return self.string[other]
        except Exception as e: 
            print(e)
            return None

    def __aiter__(self):
        return self

    async def __anext__(self):
        self._i += 1
        if self._i == len(self): 
            self._i = -1
            raise StopAsyncIteration
        return self.string[self._i]

    def __iter__(self):
        return self

    def __next__(self):
        self._i += 1
        if self._i == len(self): 
            self._i = -1
            raise StopIteration
        return self.string[self._i]

    def __int__(self):
        return int(self.string)