from os import remove, stat
import discord
from discord.ext import commands, tasks
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
import threading
from requests.api import get
import youtube_dl
import functools
import itertools
from menum import enum
from matplotlib import pyplot as plt
from matplotlib import style as matstyle
from typing import Any, Callable, Generator, Iterable, List, NoReturn, Optional, Tuple, overload, Dict, Union
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont, ImageChops

#TODO userid: gets user id given a name
#^ also channelid, emoteid, etc
__version__ = "7.10.5"
Stop = False
playingHangman = {}
playingDB = []

#CONSTS
UPTIME = time.time()
STDPrefix = "["
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
prefixFilePath = f'{DISEXT}/prefixes.txt'
achievementsFilePath = f'{DISEXT}/achievements.json'
achievementsJson = f'./achievements.json'
queuePath = "./queue"
cmdJsonFilePath = "./cmds.json"
EUROID = 334538784043696130
client = commands.Bot(command_prefix=STDPrefix, allowed_mentions=discord.AllowedMentions(everyone=False))
CMDS = {}
GENERALCHANNEL = 693893222006521856

RAMUserInfo = {}
SARCASTICQUOTES = ("mhm", "interesting", "fascinating", "very cool")
FAMILY = """
Atahan ---- Peanut                Poptoppete--------------Natalie                          Fool (the godfather)
                 |                                                            |           | 
            Kirsten (disowned)  ----------------------------- Iboy   Yavuz                                   Pen ----------------------- Troy
                                                 |                                                                                              |                 |
                                           Alison ----------------------------------------------------Sulli          Ghostly---------Cam(Tree)
                                                          |       |        |             |                |                    |         |                                    |        |
                                                       Euro May Wave Random  Custom BIS--Pals Fire                  Igor(Groot) levi------hilal
                                                                                                                              |                                                                 |     |
                                                                                                                           marios                          krogee (disowned) jabe
"""
tracemalloc.start()

class Depricated: pass
class Unused: 
    def __init__(self):...
    def __getitem__(self, other):...
class User:...
class Message:...
class fp:...
class Attachment:...
class Embed:...
class Member:...
Unused = Unused()

with open(commandusageFilePath, "r") as j:
    commandUsage = json.load(j)

with open(prefixFilePath, "r") as f:
    PREFIXES: list = f.read().split("\n")
    PREFIXES.pop(0)
    PREFIXES.insert(0, STDPrefix)

async def stop(*args: Any, **kwargs)->Union[NoReturn, Any]: #similar to how raise StopIteration works, it stops whatever is happening
    global Stop
    Stop = True
    if args: return random.choice(args)
    if kwargs.get("retstop"): return Stop

async def returnMsg(
        msg: Message, 
        content: Optional[str]=None, 
        embed: Optional[Embed]=None, 
        file: Optional[Embed]=None, 
        tts: Optional[bool]=False, 
        allowedmentions: Optional[discord.AllowedMentions]=None
    ):
    msg.content = str(content) if content is not None else ""
    msg.embeds = embed if not embed else embed
    msg.tts = tts
    msg.attachments = file
    msg.mentions = allowedmentions
    return msg

def reloadBOTMODS(ret: Optional[bool]=True)->Union[None, dict]:
    global BOTMODS
    with open(botModsFilePath, "r", encoding="utf-8-sig") as f:
        BOTMODS = json.load(f)
    if ret: return BOTMODS

async def hasPerms(userId: int, command: str)->bool:
    await UserInfo.registerUser(userId)
    return command in RAMUserInfo[int(userId)].perms

async def saveImg(filename: str, url: str)->NoReturn:
    with open(filename, 'wb') as i:
        response = requests.get(url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            i.write(block)

async def imgInChat(msg: Message, limit: Optional[int]=20)->Union[str, Tuple[Union[Attachment, str, str]]]:
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

async def getImg(msg: Message, user: Optional[User]=None, NotFromChat: Optional[bool]=False)\
->Union[Message, Tuple[Union[Attachment, str, str]]]:
    att=filename=url = None
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

async def reloadCMDSLIST(retCats: Optional[bool]=False)->dict:
    with open(customcmdsFilePath, "r") as cmdsJson:
        customCMDData = json.load(cmdsJson)
        CUSTOMCMDS = {cmd["name"]: cmd["desc"] for cmd in customCMDData}
    with open(cmdJsonFilePath, "r+") as f:
        data = json.load(f)
        CATS = [cat for cat in data.keys()]
        data["CUSTOM"]["cmds"] = customCMDData
        clearFile(f)
        json.dump(data, f)
    return CUSTOMCMDS if not retCats else CATS

def isBot(msg: Message, client: commands.Bot)->bool:
    return msg.author == client.user or msg.author.bot

async def embedToReadableDict(msg: Message, embed: Embed)->Message:
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

async def writeToFile(
        msg: Message, 
        content: str, 
        F: str, 
        sendMsg: Optional[bool]=True,
        sendAuthor: Optional[bool]=False
    )->NoReturn:
    if "." in F: 
        ext = F.split(".")[1]
        F = F.replace(f".{ext}", "")
    else: ext = "txt"
    with open(f"file.{ext}", "w", encoding="utf-8", errors="replace") as f:
        f.write(content)
    if sendMsg or sendAuthor:
        with open(f"file.{ext}", "rb") as f:
            if sendMsg: await msg.channel.send(file=discord.File(f, f"{F}.{ext}"))
            elif sendAuthor: await msg.author.send(file=discord.File(f, f'{F}.{ext}'))
    os.remove(f'file.{ext}')

async def removeFromList(l: list, *args: Any)->NoReturn:
    for arg in args: l.remove(arg)

async def formatSeconds(t: float, layer: Optional[str]="seconds", stopAt: Optional[bool]=None, rec: Optional[int]=0)\
->Tuple[float, str]:
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

def formatDateTime(createdAt: datetime.datetime, customFormatString: Optional[str]=None)->str:
    """
    %b = month name
    %d = day
    %Y = year
    %I = hour
    %M = minute
    %S = second
    %f = microsecond
    %p = am/pm
    %Z = timezone
    """
    if customFormatString:
        return createdAt.strftime(customFormatString)
    return createdAt.strftime("%b %d, %Y\nat %I:%M:%S %p")

async def getUserInContent(msg: Message, c: str, cmd: str)->User: #gets user by id, name, etc
    c = str(c.split(cmd)[1].strip())
    c = c.replace("!", "")[2:-1] if "<@" in c else c
    if not c: c = str(msg.author.id)
    user = findMember(c, msg)
    user = msg.author if not user else user
    return user

def testInContent(content: str, *testfor: str)->str:
    for x in testfor:
        if x.lower() in content.lower():
            return x
    return ""

def getCmd(content: str)->str:
    content = content.split(" ")
    if not content[0][1:]: return " "
    return content[0][1:]			

def splitContent(content: str, *split: str, index: Optional[int]=None, func=None)->str:
    for x in split:
        if x in content: #this is an IF STATEMENT, don't think it's a for loop
            ret = content.split(x)
            if func and index:
                ret = func(content.split(x)[index])
            elif func: ret = func(x)
            elif index: ret = content.split(x)[index]
            return ret
    return ""
    
def userHasRole(msg: Message, *roles: str)->bool:
    return True if discord.utils.find(lambda r: r.name in roles, msg.author.roles) else False

def findMember(c: str, msg: Message)->Member:
    return discord.utils.find(lambda m: str(m.id) == c or str(m.display_name.split("#")[0].lower()) == c.lower() or m.name.lower() == c.lower(), msg.guild.members)

def clearFile(f)->None:
    f.seek(0)
    f.truncate()

def cutCmd(string: str, returnCmd: Optional[bool]=False)->Union[Tuple[str], str]:
    cmd, *string = str(string).split(" ")
    string = " ".join(string)
    if returnCmd: return (cmd, string)
    return string

def hasPrefix(string: str, prefix: str)->bool:
    return prefix == string[:len(prefix)]

def removePrefix(string: str, prefix: str)->str:
    if not hasPrefix(string, prefix):
        return string
    return string[len(prefix):]

def hasSuffix(string: str, suffix: str)->bool:
    return hasPrefix(string[::-1], suffix[::-1]) if len(suffix) <= len(string) else False #reverses the string, and suffix so that way it can be tested as a prefix

def suitibleForEval(string: str, perms: bool=False)->bool:
    if perms: return True
    return False if ({"help(", "quit()", "exit()", "os.", "token", "input(", "sys.", "__import__(os", "time.sleep", "socket.", "exec("} & set(string.split(" "))) else True

class Content:
    def __init__(self, string: str, removeCmd: bool = True):
        for prefix in PREFIXES:
            if hasPrefix(string, prefix):
                break
        else: removeCmd = False
        if removeCmd: self.cmd, self.string = cutCmd(string, returnCmd=True)
        else: self.string = string
        self._i = -1
        self.ops_ = []
        self.opOps = []

    def calcOps(self, rep: Optional[bool]=True):
        """
        calculates -- options without yielding
        """
        if not self.split(" ") or "--" not in self: return self
        self.ops_ = tuple(word for word in self.string.split(" ")[::-1] if "--" == word.strip()[0:2] and word.strip() != "--delete")
        if rep:
            for word in self.ops_:
                foo = self.string
                self.string = self.string.replace(f' {word}', "")
                if foo == self.string:
                    self.string = self.string.replace(word, "")
        return self

    def split(self, splitBy: str, pastIndex: Optional[int]=None, key=None)->str:
        split = self.string.split(splitBy) if splitBy else list(self.string)
        if key:
            for n, s in enumerate(split):
                transformation = key(s)
                if transformation or not isinstance(transformation, bool):
                    split[n] = transformation
                else: 
                    if not transformation: split.pop(n)
        return split if not pastIndex else splitBy.join(split[pastIndex:])

    def replace(self, string: str, repWith: str): #doesn't return anything unless specified
        self.string = self.string.replace(string, repWith)
        return self
    
    def strip(self, other: Optional[str]=None)->str:
        return self.string.strip(other) if other else self.string.strip()

    def lower(self)->str:
        return self.string.lower()
    
    def testOps(self, *ops: str)->bool:
        if not self.ops_: self.calcOps()
        for op in ops:
            if op in self.opOps or op in self.ops_:
                return True
        return False
    
    def ops(self)->Generator:
        if not self.ops_: self.calcOps()
        for op in self.ops_:
            yield op

    def opsWithParams(self, paramcount: Unused[dict]=None, yieldList: Optional[bool]=False):
        """
        paramcount could be {'param': arg_num}
        or {'param': (index, split)}
        """
        #redo this so it just loops through the whole thing, keeps trakc of when the last op was, and keep appending the val to it until it reaches another
        l = self.split(" ")
        if not l[0] and len(l) < 2: return [(None, None)]
        opsDict = {}
        currOp = None
        for word in l:
            if (not word or len(word) == 1) and currOp is None: continue
            if "-" == word[0] and word[1] != "-":
                currOp = word
                opsDict[currOp] = []
                self.opOps.append(word)
            if "-" == word[0] and "-" == word[1]: break
            if currOp and word != currOp:
                opsDict[currOp].append(word)
        for op, param in opsDict.items():
            self.replace(f'{op} {" ".join(param)}'.strip(), "")
        for op, param in opsDict.items():
            if not yieldList:
                yield (op, " ".join(param))
            else: yield (op, param)

    def getUser(self, msg: Message, index: Optional[int]=None, content: Optional[str]=None)->User:
        """
        index is the index where the user should be when content is split by spaces
        """
        if index:
            try: 
                c = str(self.split(" ")[index])
                if isinstance(c, list):
                    c = " ".join(c)
                c = c.strip()
            except Exception as e: print(e); return msg.author
        else:
            try: c = str(self) if not content else str(content)
            except: return msg.author
        c = c.replace("!", "")[2:-1] if "<@" in c else c #extracts the id from string if the string is a mention
        if not c: c = str(msg.author.id)
        user = discord.utils.find(lambda m: str(m.id) == c or str(m.display_name.split("#")[0].lower()) == c.lower() or m.name.lower() == c.lower(), msg.guild.members)
        return user if user else msg.author

    def toSet(self, spl: Optional[str]=" ", pastIndex: Optional[int]=None, key=None)->set:
        """
        returns a set split by split
        """
        return set(self.split(spl, pastIndex=pastIndex, key=key))

    def suitibleForEval(self, perms: Optional[bool]=False)->bool:
        if perms: return True
        return False if ({"help(", "quit()", "exit()", "os.", "token", "input(", "sys.", "__import__(os", "time.sleep", "socket.", "exec("} & self.toSet()) else True

    def _whitespaceFormat(self, kwargs: Optional[dict]=None)->NoReturn:
        self.string = self.string.replace(r'\t', "\t")
        self.string = self.string.replace(r'\n', "\n")
        self.string = self.string.replace('\s', " ")
        self.string = self.string.replace('\z', "")
        self.string = self.string.replace(r'\b', "\b")
        if kwargs:
            for kw, arg in kwargs.items():
                self.string = self.string.replace(kw, arg)

    @staticmethod
    def whitespaceFormat(string, kwargs: Optional[dict]=None)->str:
        if kwargs:
            for kw, arg in kwargs.items():
                string = string.replace(kw, arg)
        return string.replace(r'\t', "\t").replace(r'\n', "\n").replace("\s", " ").replace("\z", "").replace(r'\b', "\b")

    def formatMessage(self, msg: Message, kwargs: Optional[dict]=None, removeCmd: Optional[bool]=True, ret: Optional[bool]=False)->Union[None, Any]:
        if "{emote}" in self:
            new = [x if x.strip() != "{emote}" else str(random.choice(msg.guild.emojis)) for x in self.split(" ")]
            self.string = " ".join(new)
        self.string = self.string.replace("{content}", str(Content(msg.content, removeCmd=removeCmd)))
        self.string = self.string.replace("{version}", __version__)
        self.string = self.string.replace("{authorn}", msg.author.name).replace("{author}", msg.author.mention)
        self.string = self.string.replace("{authorid}", str(msg.author.id))
        self.string = self.string.replace("{uptime}", str(time.time() - UPTIME))
        if "{formattime " in self.string:
            for formatTime in self.string.split("{formattime"):
                if "}" not in formatTime: continue
                ft = formatTime.split("}")[0].strip()
                formatTime = formatDateTime(msg.created_at, customFormatString=ft)
                self.string = self.string.replace("{formattime %s}" %ft, formatTime)
        if not isinstance(msg.channel, discord.DMChannel): 
            self.string = self.string.replace("{channeln}", msg.channel.name).replace("{channel}", msg.channel.mention).replace("{channelid}", str(msg.channel.id))
        if kwargs:
            for k, i in kwargs.items():
                self.string = self.string.replace(str(k), str(i))
        if ret: return self

    def insert(self, index: int, other: str)->NoReturn:
        foo = list(self)
        foo.insert(index, other)
        self.string = "".join(foo)

    def __len__(self):
        return len(self.string)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.string)

    def __add__(self, other):
        return self.string + other

    def __iadd__(self, other):
        return self + other

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

    def __setitem__(self, index, other):
        foo = self.split("")
        foo[index] = other
        self.string = "".join(foo)

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

    def __float__(self):
        return float(self.string)  

    def __case__(self, case):
        return self @ case

class switch:
    def __init__(self, value):
        self.value = value
        if "__case__" in dir(value):
            self.__case__ = value.__case__

    def start(self):
        return self

    def end(self):
        del self

    def __case__(value, other):
        if isinstance(other, list) or isinstance(other, tuple):
            return value in other
        
    def __call__(self, other, *args, **kwargs):
        if not isinstance(other, list): return self.value == other
        return self.__case__(other, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.end()

class FileException(Exception):
    pass

class command:
    category: str = None
    categoryDesc: str = None
    def __init__(self, func):
        self.func = func
        self.aliases = []
        self.secretAliases = []
        self.doc = func.__doc__
        self.cat = command.category
        self._Help = False
        doc = func.__doc__
        name = func.__name__.lower()
        CMDS[name] = self
        aliasList = self.aliases
        if "CATEGORY: " in doc:
            self.cat = doc.split("CATEGORY: ")[1].split("\n")[0].strip().upper()
        if len(doc.split("aliases")) > 1:
            aliases = doc.split("aliases:")[1].split("\n")
            for alias in aliases:
                if alias != " ": alias = alias.strip()
                if alias:
                    if "added" in alias: 
                        self.date = alias.split("added")[1].strip().strip(":").strip()
                        break
                    if "CATEGORY: " in alias:
                        self.cat = alias.split("CATEGORY: ")[1].split("\n")[0].strip().upper()
                        self.doc = self.doc.replace(f"CATEGORY: {self.cat}", "")
                        break
                    if "SECRET" in alias:
                        aliasList = self.secretAliases
                        continue
                    CMDS[alias] = self
                    if aliasList is self.secretAliases:
                        self.secretAliases.append(alias)
                    else: self.aliases.append(alias)
        self.__addCmd()

    async def __call__(self, *args, **kwargs):
        msg, content = args
        cmd = kwargs.get("cmd")
        print(f'{msg.author.name}: {cmd}({content})')
        return await self.func(*args, **kwargs)

    def calcHelp(self)->NoReturn:
        helpMsg = self.doc
        if "WHITESPACEFORMATS" in helpMsg: helpMsg += "\ndo help whitespaceformats for more information"
        if "FORMATS" in helpMsg: helpMsg += "\ndo help formats for more information"
        desc = ""
        requiredParams = ""
        optionalParams = ""
        options = ""
        added = ""

        helpMsgTemp = helpMsg.split("\n")
        if not helpMsgTemp[0]: helpMsgTemp = helpMsgTemp[1:]
        if "CUSTOM:" not in helpMsgTemp[0]:
            for line in helpMsgTemp:
                if "added" in line or "params" in line or "options" in line or "aliases" in line:
                    break
                desc += line.strip() + "\n"

            helpMsgRequired = helpMsg.split("required params")
            if len(helpMsgRequired) > 1:
                helpMsgRequired = helpMsgRequired[1].split("\n")
                for line in helpMsgRequired:
                    if "added" in line or "params" in line or "options" in line or "aliases" in line:
                        break
                    requiredParams += line.strip().strip(":") + "\n"

            helpMsgOptional = helpMsg.split("optional params")
            if len(helpMsgOptional) > 1:
                helpMsgOptional = helpMsgOptional[1].split("\n")
                for line in helpMsgOptional:
                    if "added" in line or "params" in line or "options" in line or "aliases" in line:
                        break
                    optionalParams += line.strip().strip(":") + "\n"

            helpMsgOptions = helpMsg.split("options")
            if len(helpMsgOptions) > 1:
                helpMsgOptions = helpMsgOptions[1].split("\n")
                for line in helpMsgOptions:
                    if "added" in line or "params" in line or "options" in line or "aliases" in line:
                        break
                    options += line.strip().strip(":") + "\n"

            helpMsgAdded = helpMsg.split("added")
            if len(helpMsgAdded) > 1:
                added = helpMsgAdded[1].strip().strip(":").strip()
            newLine = "\n"
            helpMsg = f'**```{desc}```**'
            self.desc = desc
            if requiredParams:
                helpMsg += f"```required params:{requiredParams}```"
                self.requiredParams = requiredParams
            if optionalParams:
                helpMsg += f"```optional params:{optionalParams}```"
                self.optionalParams = optionalParams
            if options:
                helpMsg += f"```options:{options}```"
                self.options = options
            if self.aliases:
                helpMsg += f"```aliases:{newLine + newLine.join(self.aliases)}```"
            if added:
                helpMsg += f"```added:{added}```"
                self.added = added
            helpMsg += f'```Category: {self.cat}```'
            self._Help = helpMsg
        else:
            helpMsgTemp = helpMsgTemp[1:]
            self._Help = "\n".join(helpMsgTemp)

    def help(self):
        if not self._Help: self.calcHelp()
        return self._Help

    def __addCmd(self):
        with open(cmdJsonFilePath, "r+") as f:
            data = json.load(f)
            data[self.cat]["cmds"].append(self.func.__name__.lower())
            for alias in self.aliases:
                if alias not in data[self.cat]["cmds"]:
                    data[self.cat]["cmds"].append(alias)
            clearFile(f)
            json.dump(data, f)

    @classmethod
    def setCategory(cls, category: str, categoryDesc: str):
        cls.category = category.upper()
        cls.categoryDesc = categoryDesc
        with open(cmdJsonFilePath, "r+") as f:
            data = json.load(f)
            if not data.get("KEY"):
                data["KEY"] = {"desc": "FORMATS formats special phrases with something (WHITESPACE FORMATS) formats whitespaces\ndo [help formats and [help whitespaceformats", "cmds": []}
                data["ANYMESSAGE"] = {"desc": "can be applied to any message", "cmds": ["[timeit", "[chkx", "[delete", "[rw", "[rwd", "[delin", "[dr"]}
                data["MOSTCMDS"] = {"desc": "works for most if not all commands", "cmds": ["--delete", ">>>", "--cmddelete\ndeletes on the command instead of when you send", "--help (DEPRICATED)", "<<<", "cmd--[optional]\nreplaces cmd-- with -- (works like --cmddelete)"]}
                data["SYNTAX"] = {"desc": "acts like a programming language", "cmds": ["for", "if", "else", "wait", "*<cmd> (sep with ;;)", "calc", "eval", "result", "equation", "findans", "exec", "/{}", "cmd/{}"]}
                data["CUSTOM"] = {"desc": "custom commands", "cmds": []}
            data[cls.category] = {}
            data[cls.category]["desc"] = cls.categoryDesc
            data[cls.category]["cmds"] = []
            clearFile(f)
            json.dump(data, f)

def getAchievement(id_: int=None, name: str=None, desc: str=None):
    with open(achievementsJson, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        for achievement in data:
            if achievement["id"] == id_:
                return achievement
            elif achievement["name"] == name:
                return achievement
            elif achievement["desc"] == desc:
                return achievement

async def sayMessage(msg: discord.Message, content: str=None, embed: discord.Embed=None)->NoReturn:
    await msg.channel.send(content, embed=embed)

class UserInfo:
    def __init__(self, userId):
        self.userId = str(userId)
        RAMUserInfo[self.userId] = self
        self.cmdsIn30Seconds = 0
        self.timeLastCmdUsed = 0
        #leveling data
        with open(levelingDataFilePath, "r", encoding="utf-8-sig") as j:
            levelingInfo = json.load(j).get(self.userId)
        if levelingInfo:
            self.level = levelingInfo["level"]
            self.xp = levelingInfo["xp"]
            self.required = levelingInfo["required"]
            self.lastTalked = levelingInfo["lastTalked"]
            self.levelUpMessage = levelingInfo.get("message")
            if not self.levelUpMessage:
                self.levelUpMessage = '{author} you have leveled up to level {level}, very cool'
            del levelingInfo
        else:
            self.level = 0
            self.xp = 0
            self.required = 1000
            self.lastTalked = time.time()
            self.levelUpMessage = "{author} you have leveld up to level {level}, very cool"
        self.levelUpMessage = Content(self.levelUpMessage, removeCmd=False)

        #pingresponse
        with open(pingResponseFilePath, "r", encoding="utf-8-sig") as j:
            pr = json.load(j).get(self.userId)
            if pr:
                self.pingResponse = pr.get("response")
                self.pingResponseWhen = pr.get("when")
            else: 
                self.pingResponse = ""
                self.pingResponseWhen = []

        #bans
        with open(bannedFilePath, "r", encoding="utf-8-sig") as j:
            bannedInfo = json.load(j).get(self.userId)
            self.bans = bannedInfo if bannedInfo else []

        #timers
        with open(timersPath, "r", encoding="utf-8-sig") as j:
            timers = json.load(j).get(self.userId)
            self.time = timers if timers else 0

        #money
        with open(moneyDataFilePath, "r", encoding="utf-8-sig") as j:
            money = json.load(j).get(self.userId)
            self.money = money if money else 0

        #items
        with open(itemDataFilePath, "r", encoding="utf-8-sig") as j:
            items = json.load(j).get(self.userId)
            self.items = items if items else {}
            if type(self.items) is list:
                t = {}
                for item in self.items:
                    try: t[item["name"]] += 1
                    except: t[item["name"]] = 1
                self.items = t
        #perms
        with open(botModsFilePath, "r", encoding="utf-8-sig") as j:
            perms = json.load(j).get(self.userId)
            self.perms = perms if perms else []

        #achievements
        with open(achievementsFilePath, "r", encoding="utf-8-sig") as j:
            achievements = json.load(j).get(self.userId)
            self.achievements = []
            if achievements:
                for achievement in achievements:
                    if isinstance(achievement, dict):
                        self.achievements.append(getAchievement(id_=achievement["id"])["id"])
                    else:
                        self.achievements.append(achievement)

    async def giveAchievement(self, msg, achievement: Union[int, str, dict]):
        """
        if achievement is a dict, it will assume achievement
        is valid and will not search for achievement
        """
        if isinstance(achievement, str):
            achievement = getAchievement(name=achievement)
        elif isinstance(achievement, int):
            achievement = getAchievement(id_=achievement)
        if achievement["id"] not in self.achievements:
            self.achievements.append(achievement["id"])
            await sayMessage(msg, content=achievement["onget"]["message"])
            if achievement["onget"].get("money"):
                await self.addMoney(achievement["onget"]["money"])

    async def usedCmd(self, msg: Message)->bool:
        if time.time() - self.timeLastCmdUsed <= 30 and msg.channel.id == GENERALCHANNEL:
            self.cmdsIn30Seconds += 1
        else: self.cmdsIn30Seconds = 0
        if self.cmdsIn30Seconds >= 7 and msg.channel.id == GENERALCHANNEL:
            await msg.channel.send("hey there buddy chum pal friend buddy pal chum bud friend fella bruther amigo pal buddy friend chummy chum chum pal. i don't mean to be rude my friend pal homeslice breadslice dawg, but you should probably move this to <#732071485564256377> my friend buddy chum friendly friend friend pal friend buddy chum pally friend chum buddy.")
            return False
        self.timeLastCmdUsed = time.time()
        return True

    async def giveXP(self, msg: Message)->Union[None, NoReturn]:
        if time.time() - self.lastTalked >= 60:
            self.xp += random.randint(15, 100)
            self.lastTalked = time.time()
            if self.xp >= self.required:
                self.level += 1
                if self.level == 100:
                    self.giveAchievement(msg, 3)
                self.xp //= 2
                self.money += int(self.level * 2)
                temp = Content(self.levelUpMessage, removeCmd=False)
                temp.formatMessage(msg, {"{level}": self.level, "{xp}": self.xp}, removeCmd=False)
                disp = str(temp)
                if disp and disp.lower() not in ["none", "null"]:
                    await msg.channel.send(disp)
                self.required = round((1000 * self.level) * 1.1)
        else: return

    async def dumpLevelInfo(self)->NoReturn:
        with open(levelingDataFilePath, "r+", encoding="utf-8-sig") as j:
            data = json.load(j)
            data[self.userId] = {
                "level": self.level,
                "xp": self.xp,
                "required": self.required,
                "lastTalked": self.lastTalked,
                "message": str(self.levelUpMessage)
            }
            clearFile(j)
            json.dump(data, j)

    async def basicDump(
            self, 
            file: str, 
            attrToDump: str, 
            encoding: Optional[str]="utf-8-sig", 
            DumpIfNone: Optional[bool]=True
        )->NoReturn:
        DelData = DumpIfNone^1
        with open(file, "r+", encoding=encoding) as j:
            data = json.load(j)
            if attrToDump or DumpIfNone:
                data[self.userId] = attrToDump
            if (not attrToDump and not DumpIfNone) and DelData:
                if data.get(self.userId):
                    del data[self.userId]
            clearFile(j)
            json.dump(data, j)

    async def dumpMoneyInfo(self)->NoReturn:
        await self.basicDump(moneyDataFilePath, self.money)

    async def dumpAchievementInfo(self)->NoReturn:
        with open(achievementsFilePath, "r+", encoding="utf-8-sig") as j:
            data = json.load(j)
            data[self.userId] = self.achievements
            clearFile(j)
            json.dump(data, j)

    async def dumpBannedInfo(self)->NoReturn:
        await self.basicDump(bannedFilePath, self.bans, DumpIfNone=False)

    async def dumpTimerInfo(self)->NoReturn:
        if not self.time: 
            with open(timersPath, "r+", encoding="utf-8-sig") as f:
                data = json.load(f)
                try: del data[self.userId]
                except: pass
                finally:
                    clearFile(f)
                    json.dump(data, f)
        else: await self.basicDump(timersPath, self.time)

    async def dumpItemInfo(self)->NoReturn:
        await self.basicDump(itemDataFilePath, self.items, DumpIfNone=False)
            
    async def dumpPermInfo(self)->NoReturn:
        await self.basicDump(botModsFilePath, self.perms, DumpIfNone=False)

    async def dumpPingResponseInfo(self)->NoReturn:
        with open(pingResponseFilePath, "r+") as f:
            data = json.load(f)
            if data.get(self.userId):
                if not self.pingResponse:
                    del data[self.userId]
                else:
                    data[self.userId] = {"response": self.pingResponse, "when": self.pingResponseWhen}
                clearFile(f)
                json.dump(data, f)
            
    async def dumpInfo(self, clFromRAMDict: Optional[bool]=False)->NoReturn:
        await self.dumpLevelInfo()
        await self.dumpMoneyInfo()
        await self.dumpBannedInfo()
        await self.dumpTimerInfo()
        await self.dumpItemInfo()
        await self.dumpPermInfo()
        await self.dumpPingResponseInfo()
        await self.dumpAchievementInfo()
        if clFromRAMDict: await self.clearFromRAMDict()

    async def clearFromRAMDict(self)->NoReturn:
        del RAMUserInfo[int(self.userId)]
    async def reduceXP(self)->NoReturn:
        if time.time() - self.lastTalked >= 1209600:
            if self.xp > 1:
                self.xp -= random.randint(0, 1)
            if self.xp <= (self.level * 1000) // 2 and self.level > 1:
                self.level -= 1
                self.xp = (self.level * 1000) - 1

    async def addMoney(self, amnt: int)->NoReturn:
        self.money += amnt
        
    async def removeItem(self, iName: Optional[str]=None, iId: Optional[int]=None, item: Optional[dict]=None)->NoReturn:
        if not item: item = findItem(iName=iName, iId=iId)
        self.items[item["name"]] -= 1
        if not self.items[item["name"]]:
            del self.items[item["name"]]

    @classmethod
    async def registerUser(cls, userId: Union[int, str])->NoReturn:
        userId = int(userId)
        if userId not in RAMUserInfo.keys():
            RAMUserInfo[userId] = cls(userId)
            
class _Dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __getattribute__(self, name):
        try: return self[name]
        except: return None

def findItem(iName: Optional[str]=None, iId: Optional[int]=None)->dict:  
    with open(itemsFilePath, "r") as f:
        data = json.load(f)
        for item in data:
            if item["id"] == iId or item["name"] == iName:
                return item

def totalMoney(RAMUserInfo: Dict[int, UserInfo]):
    total = sum(map(lambda user: user.money, RAMUserInfo.values()))
    return total

objects = _Dict()

token = "NjQxNzk1NjU2Mzc3MTcyMDAw.XcNk8g.HEvnaXjuXFQhN1iilaaffbiPcoo"