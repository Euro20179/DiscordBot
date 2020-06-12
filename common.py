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

DELETE = "--delete"
VERSION = "4.0.9"
Stop = False

playingGuessingGame = {}
runningStopwatch = {}
playingHangman = {}
playingDB = []

#CONSTS
PREFIX = "]"
token = "NjQxNzk1NjU2Mzc3MTcyMDAw.XcNk8g.HEvnaXjuXFQhN1iilaaffbiPcoo"
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
itemsFilePath = f'items.json'
EUROID = 334538784043696130
client = commands.Bot(command_prefix=PREFIX)

tracemalloc.start()

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
        print(CUSTOMCMDS)
    return CATS, CMDLIST, CUSTOMCMDS