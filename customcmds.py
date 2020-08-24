from common import *


@command
async def addCustomCmd(msg, content, cmd="customcmd"):
    """
    adds a custom command
    required params:
        <cmd name>| <say>:
            the name of the command | what the command says
            do {} to do a command inside it and replace it with the result
    options:
        --lock: makes it so only you and people with botmod of eccmd can edit the command
    FORMATS when using the command
    aliases:
        accmd
        customcommand
        addcustomcmd
    added: 6/11/2020
    """
    global CUSTOMCMDS
    content = Content(content)
    Locked = False if not content @ "--lock" else True
    c = content.split("|")
    name = c.pop(0).strip()
    say = "|".join(c)
    if " " in name: return await returnMsg(msg, "no spaces in command names")
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for cmd in data:
            if cmd["name"] == name:
                return await returnMsg(msg, "already a command")
        params = ""
        if "{content}" in say:
            params += " <message>"
        if datetime.datetime.now().strftime("%Y") == "2020":
            d = datetime.datetime.now().strftime("%m/%d/%Y")
        else:
            d = datetime.datetime.now().strftime("%m/%d/%y")
        data.append({"name": name, "desc": say, "params": params, "date": d, "Locked": Locked, "addedby": str(msg.author.id), "editedby": []})
        mssg = await returnMsg(msg, "added")
        clearFile(j)
        json.dump(data, j)
    CUSTOMCMDS = await reloadCMDSLIST()
    return mssg

@command
async def removeCustomCmd(msg, content, cmd="removecustomcmd"):
    """
    removes a custom command, must have botmod or can manage messages
    required params:
        <cmd name>: the command name to remove
    aliases:
        removecustomcmd
        delcustomcmd
        rccmd
        dccmd
    added: 6/11/2020
    """
    global CUSTOMCMDS
    perms = msg.author.guild_permissions.manage_messages
    if not perms and not await hasPerms(msg.author.id, cmd):
        return await returnMsg(msg, "you cannot do that")
    name = content[len(cmd) + 2:].split(" ")
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for cmd in data:
            if cmd["name"] in name:
                if cmd.get("Locked"):
                    try:
                        await msg.channel.send(f"{msg.author.mention} this command is locked are you sure")
                        YN = await client.wait_for("message", check=lambda message: message.author.id == msg.author.id, timeout=60.0)
                    except:
                        return await returnMsg(msg, "cancelled")
                    if YN.content.lower() in ["no", "cancel", 'stop', 'n']:
                        return await returnMsg(msg, "cancelled")
                data.remove(cmd)
                name.remove(cmd["name"])
        if name: return await returnMsg(msg, f"{', '.join(name)} not found")
        clearFile(j)
        json.dump(data, j)
    CUSTOMCMDS = await reloadCMDSLIST()
    return await returnMsg(msg, f'removed {" ".join(name)}')

@command
async def editCustomCmd(msg, content, cmd="eccmd"):
    """
    edits a specified command
    required params:
        <cmd name>|<new>:
            the command to edit, what it should say
    options:
        --lock: instead of doing <new> you can do lock to lock/unlock a command
    aliases:
        editcustomcmd
        eccmd
    added: 6/13/2020
    """
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    content = Content(content)
    lookFor = content.split("|")[0].strip()
    changeTo = content.split("|", pastIndex=1)
    with open(customcmdsFilePath, "r+") as j:
        data = json.load(j)
        for command in data:
            if command["name"] == lookFor:
                if command.get("Locked"):
                    if not await hasPerms(str(msg.author.id), cmd) and not str(msg.author.id) == command.get("addedby"):
                        return await returnMsg(msg, "cannot change that command it's locked")
                if "--lock" in changeTo:
                    if not command.get("Locked"):
                        command["Locked"] = True
                    else: command["Locked"] ^= True
                else:
                    command["desc"] = changeTo
                if command.get("editedby"):
                    if str(msg.author.id) not in command["editedby"]:
                        command["editedby"] += [str(msg.author.id)]
                else: command["editedby"] = [str(msg.author.id)]
                break
        else: return await returnMsg(msg, "command doesn't exist")
        clearFile(j)
        json.dump(data, j)
    return await returnMsg(msg, "changed successfully")

@command
async def customCmdList(msg, content, cmd="customcmdlist"):
    """
    lists the custom commands
    options:
        --raw: the raw json file
        --file: get a file of the cmds
    aliases:
        ccmdlist
        customcmdlist
    added: 6/11/2020
    """
    CUSTOMCMDS = await reloadCMDSLIST()
    content = Content(content)
    if content @ "--raw":
        with open(customcmdsFilePath, "rb") as f: await msg.channel.send(file=discord.File(f, "customCmds.json"))
    else:
        try:
            if content @ "--file": raise FileException("wanted file")
            content = await msg.channel.send("\n".join([f'{x}: {y}' for x, y in CUSTOMCMDS.items()]))
        except:
            write = ""
            with open(customcmdsFilePath, "r") as j:
                data = json.load(j)
                for cmmd in data:
                    params = cmmd["params"]
                    desc = cmmd["desc"]
                    aliases = cmmd.get("aliases")
                    date = cmmd.get("date")
                    Locked = cmmd.get("Locked")
                    addedBy = cmmd.get("addedby")
                    editedBy = cmmd.get("editedby")
                    if aliases: aliases = ",\n".join(f'``{x}``' for x in aliases)
                    write += f'Name {cmmd["name"]}\n\nParams: {params}\n\nDescription: {desc}\n\nAliases: {aliases}\n\nDate added: {date}\n\nLocked: {Locked}\n\nAdded by: {addedBy}\n\nEdited by: {editedBy}\n\n\n\n'
            with open("customcmdlist.txt", "w") as f:
                f.write(write)
            with open("customcmdlist.txt", "rb") as f:
                await msg.channel.send(file=discord.File(f, "customcmdlist.txt"))
            os.remove("customcmdlist.txt")
