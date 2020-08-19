from common import *

@command
async def ridInvites(msg, content, cmd="clearinvites"):
    """
    removes all active server invites
    added: 5/30/2020
    """
    perms = msg.author.guild_permissions.create_instant_invite
    if perms:
        invites = await msg.guild.invites()
        for inv in invites:
            await inv.delete()
        return await returnMsg(msg, "invites cleared")
    else: return await returnMsg(msg, "you don't have perms")


@command
async def clear(msg, content, cmd="clear"):
    """
    clears <amount> of messages in chat
    must have message edit perms to use this
    (don't abuse :)))))
    required params:
        <amount>: the amount of messages
    options:
        -user <user>: the user who's messages to delete
        -len <length of message>: the length of the message or longer that gets deleted
    added: 11/6/19
    """
    content = Content(content)
    user = None
    length = None
    for op, param in content.opsWithParams({"user": (slice(0,None,None), " ")}):
        if op == "-user":
            user = content.getUser(msg, content=" ".join(param))
        if op == "-len":
            length = param
    amnt = int(content)
    if isBot(msg, client): return await returnMsg(msg, "nope")
    perms = msg.author.guild_permissions.manage_messages
    if perms and msg.author.id != 579117856994623498:
        if user and length: await msg.channel.purge(limit=amnt, check=lambda x: len(x.content) < int(length) and x.author == user)
        elif user:
            await msg.channel.purge(limit=amnt, check=lambda x: x.author == user)
        elif length:
            await msg.channel.purge(limit=amnt, check=lambda x: len(x.content) > int(length))
        else: await msg.channel.purge(limit=amnt)
    else:
        await msg.channel.send(f"{msg.author.mention} you can't do that")
        for _ in range(random.randint(10, 15)):
            await msg.author.send("you cannot do that, don't do it again")

@command
async def mballDel(msg, content, cmd="8brdel"):
    """
    removes an 8ball reply you must have perms to be able to use this
    required params:
        <reply>: the reply to remove
    aliases:
        mballdel
        8brdel
    """
    global BOTMODS
    BOTMODS = reloadBOTMODS()
    reply = str(Content(content))
    if str(msg.author.id) in BOTMODS.keys():
        if cmd in BOTMODS[str(msg.author.id)]:
            with open(mballresponseFilePath, "r+") as f:
                replies = f.read().split("\n")
                if reply in replies:
                    replies.remove(reply)
                    clearFile(f)
                    f.write("\n".join(replies))
                    return await returnMsg(msg, f'removed message: {reply}')
                else: return await returnMsg(msg, "not a message")
    else: return await returnMsg(msg, "you don't have perms")
