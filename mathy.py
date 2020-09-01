from common import *


@command
async def weightedCoin(msg, content, cmd="weightedcoin"):
    """
    flips a weighted coin
    required params:
        <heads odds>: the odds of landing on heads
    optional params:
        [times]: the times to flip the coin (limit of 10000000)
    added: 6/30/2020
    """
    content = Content(content).split(" ")
    headsOdds = content[0]
    if len(content) > 1:
        flips = content[1]
    else: flips = 1
    UseC = "," in flips
    if UseC: flips = flips.replace(",", "")
    try: headsOdds = float(headsOdds)
    except: return await returnMsg(msg, "not a number")
    if headsOdds > 1 or headsOdds < 0:
        return await returnMsg(msg, "odds must be less than 1 and greater than 0")
    if int(flips) > 1 and int(flips) < 10000000:
        heads = 0
        tails = 0
        for _ in range(int(flips)):
            if random.random() > .5: heads += 1
            else: tails += 1
        embed = discord.Embed(title=f'Heads: {format(heads, ",d") if UseC else heads}\nTails: {format(tails, ",d") if UseC else tails}', color=0x00ff00)
    else:
        ans = "heads" if random.random() <= headsOdds else "tails"
        embed = discord.Embed(title=ans, color=0xff00ff if ans == "heads" else 0x0000ff)
    return await returnMsg(msg, embed=embed)

@command
async def choose(msg, content, cmd="choose"):
    """
    choses -picks amount of <choices>, defaults to 1 pick
    required params:
        *<choices> (sep with |): the items it can pick from
    options:
        -picks <amount>: the amount of times it chooses
        -sep <sep by> (WHITESPACEFORMATS): what the answers are seperated by
    added: 5/6/2020
    """
    content = Content(content)
    opOps = list(content.opsWithParams())
    sep = " | "
    picks = 1
    for op, param in opOps:
        if op == "-picks": picks = int(param)
        elif op == "-sep":
            sep = Content.whitespaceFormat(param)
    options = content.split("|", key=lambda x: x.strip())
    return await returnMsg(msg, sep.join([random.choice(options) for _ in range(picks)]))

@command
async def coin(msg, content, cmd="coin"):
    """
    flips a coin
    optional params:
        [h/t]: bet heads/tails (cannot specify flips if this is chosen)
        [flips]: the amount of times to flip the coin (limit of 10000000)
    added: 1/18/2020
    """
    title = res = "heads" if random.random() >= .5 else "tails"
    if " " in content:
        bet = content.split(" ")[1].strip()
        UseC = "," in bet
        if UseC: bet = bet.replace(",", "")
        if bet == "t": bet = "tails"
        if bet == "h": bet = "heads"
        if not bet.isnumeric() and not UseC:
            color, title = (0x00ff00, "YOU WIN") if res == bet else (0xff0000, "YOU LOSE")
            add = random.randint(1, 3) if res == bet else random.randint(-3, -1)
            await RAMUserInfo[msg.author.id].addMoney(add)
            title += f'\nYOU WON {add}' if res == bet else f'\nYOU LOSE {abs(add)}'
        elif int(bet) < 10000000:
            heads = 0
            tails = 0
            for _ in range(int(bet)):
                if random.random() > .5: heads += 1
                else: tails += 1
            embed = discord.Embed(title=f'Heads: {format(heads, ",d") if UseC else heads}\nTails: {format(tails, ",d") if UseC else tails}', color=0x00aa00)
            return await returnMsg(msg, embed=embed)
    color = 0xff00ff if res == "heads" else 0x0000ff
    embed = discord.Embed(title=title, color=color)
    return await returnMsg(msg, embed=embed)

@command
async def rand(msg, content, cmd="rand"):
    """
    picks a random number from <low> to <high>
    if you put a , in low or high, the result will have , in it
    required params:
        <low>: the low number
        <high>: the high number
    optional params:
        [round]: the amount of places to round to
            only give if low or high is a decimal
    options:
        --even: makes the result even
        --odd: makes the result odd
    added: 1/18/2020
    """
    content = Content(content)
    Even = content @ "--even"
    Odd = content @ "--odd"
    UseC = True if "," in content else False
    content.replace(",", "")
    content = content.split(" ")
    low = 1
    high = 10
    r = 0
    if len(content) > 1:
        r = int(content[2].strip()) if len(content) == 3 else 0
        low, high = float(content[0]), float(content[1])
        try: int(r)
        except: return await returnMsg(msg, "you are not rounding to a whole number")
        if float(low) >= float(high): return await returnMsg(msg, "Low must be lower than high")
    while True:
        res = random.uniform(low, high)
        if Even and int(round(res, r)) % 2 != 0 and r == 0: continue
        if Odd and int(round(res, r)) % 2 == 0 and r == 0: continue
        else: break
    res = int(round(res, r)) if r == 0 else round(res, r)
    if UseC and not isinstance(res, float):
        res = format(res, ',d')
    return await returnMsg(msg, res)

@command
async def hexCmd(msg, content, cmd="hex"):
    """
    generates the hex form of each num given
    required params:
        *<num>
    aliases:
        hex
    added: 5/21/2020
    """
    ans = map(lambda n: str(hex(int(n))), Content(content).split(" "))
    return await returnMsg(msg, ", ".join(ans))

@command
async def octCmd(msg, content, cmd="oct"):
    """
    generates the oct form of each num given
    required params:
        *<num> 
    aliases:
        oct
    added: 5/27/2020
    """
    ans = map(lambda n: str(oct(int(n))), Content(content).split(" "))
    return await returnMsg(msg, ", ".join(ans))

@command
async def binCmd(msg, content, cmd="bin"):
    """
    generates the binary form of each num given
    required params:
        *<num>
    aliases:
        bin
    added: 5/21/2020
    """
    ans = map(lambda n: str(bin(int(n))), Content(content).split(" "))
    return await returnMsg(msg, ", ".join(ans))

@command
async def toKelvin(msg, content, cmd="tok"):
    """
    calculates <temp> to kelvin
    example: [tok 60f
    required params:
        *<temp[from]>: the tempurature
            [from]: the unit to convert from
                ex: [tok 40f
                ex: [tok 40f 40c
    optional params:
        [from]: c/f to make all the temps that unit
            ex: [tok 50 23 f
    options:
        -sep <seperator>: what to seperate each answer by
    aliases:
        tokelvin
        tok
    added: 7/14/2020
    """
    content = Content(content)
    sep = "\n"
    for op, param in content.opsWithParams():
        if op == "-sep":
            sep = Content.whitespaceFormat(param)
    content = content.string.split(" ")
    if content[-1].isalpha():
        overAllT = content[-1]
    else: overAllT = "c"
    answers = []
    for temp in content:
        t = {"f" in temp: "f", "c" in temp: "c"}.get(True)
        if not t: t = overAllT
        temp = temp.replace(t, "").strip()
        if not temp: continue
        ans = str((9 / 5 * float(temp) + 32) + 273 if t == "f" else float(temp) + 273)
        answers.append(ans)
    return await returnMsg(msg, sep.join(answers))

@command
async def toc(msg, content, cmd="toc"):
    """
    converts farenheight to celcius
    required params:
        *<temp>
    options:
        -sep <seperator>: the chars to seperate each temp by
    """
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-sep": 
            sep = Content.whitespaceFormat(param)
            break
    else: sep = "\n"
    temps = map(lambda t: str((5 / 9) * float(t)), content.strip().split(" "))
    return await returnMsg(msg, sep.join(temps))

@command
async def tof(msg, content, cmd="tof"):
    """
    converts celcius temp to farenheight
    required params:
       *<temp>: the temp to convert from
    options:
        -sep <seperator>: the chars to seperate each temp by
    """
    content = Content(content)
    for op, param in content.opsWithParams():
        if op == "-sep": 
            sep = Content.whitespaceFormat(param)
            break
    else: sep = "\n"
    temps = map(lambda t: str((9 / 5) * float(t)), content.strip().split(" "))
    return await returnMsg(msg, sep.join(temps))

@command
async def dice(msg, content, cmd="dice"):
    """
    rolls a dice that defaults with 6 sides
    optional params:
        [sides]: the number of sides the dice has
        [side expression]: the equation to figure out each side's value, must provide the amount of sides to use this
    options:
        -sep <seperator>: what to seperate each roll by
        -rolls <count>: the amount of times to roll
        --eval: the choices will be the eval of [side expression] instead of applying a number in place of n for each side
    aliases:
        dice
        roll
    added: 8/6/2020
    """
    content = Content(content.strip())
    rollCount = 1
    sep = "\n"
    for op, param in content.opsWithParams():
        if op == "-rolls": 
            rollCount = int(param)
        elif op == "-sep":
            sep = Content.whitespaceFormat(param)
    content = content.strip().split(" ")
    high = int(content[0]) if content[0] else 6
    FullEval = False
    if len(content) > 1:
        evalStmnt = Content(" ".join(content[1:]), removeCmd=False)
        FullEval = evalStmnt @ "--eval"
        if not evalStmnt.suitibleForEval():
            return await returnMsg(msg, "nice try")
    else: evalStmnt = "n"
    if not FullEval:
        choices = tuple(eval(str(evalStmnt)) for _ in range(1, high))
        rolls = tuple(str(random.choice(choices)) for _ in range(rollCount))
    else:
        rolls = [str(random.choice(eval(str(evalStmnt)))) for _ in range(rollCount)]
    return await returnMsg(msg, sep.join(rolls))

@command
async def calc(msg, content, cmd="calc", ReturnRes=False):
    """
    gives the answer to an expression
    required params:
        <equation>: the equation/expression to evaluate
            most things should work but power is ** not ^
    aliases:
        eval
        result
        equation
        findans
        calc
    added: 5/23/2020
    """
    content = Content(content)
    if not content.suitibleForEval(perms=await hasPerms(msg.author.id, cmd)):
        return await returnMsg(msg, 'nice try')
    else:
        if str(content) in ["1 + 1", "1+1"]:
            return await returnMsg(msg, "1 + 1 = window")
        elif str(content) in ["2 + 2", "2+2"]:
            return await returnMsg(msg, "2 + 2 = fish")
        try:
            rv = eval(str(content))
            if not ReturnRes: return await returnMsg(msg, rv)
            else: return rv
        except Exception as e:
            print(e)
            return await returnMsg(msg, str(type(e)).split(' ')[1].split("'")[1].strip("'"))

@command
async def graph(msg, content, cmd="graph"):
    """
    CUSTOM:
```
graphs a line``````required params:
*<equation> (sep with |):
    ex: [graph x^2
    (to use bitwise xor do **)``````options:
-range <amnt : number>: basically how long the x axis is
-lstyle <style>: the style of the line
-marker <marker>: what to mark each point with
-color <color>: the color of the line
-fillstyle <style>: idk what this does
-alpha <alpha of line 0-1>: the alpha of the line
-gstyle <style>: the style of the graph
-drawstyle <style>: drawstyle
-markersize <size : decimal>: the size of each marker
-scatter *<points : (x, y)>: makes it a scatter instead of line graph (equation not used)
--scatter: uses the equation, but makes a scatter graph
NOTE: when using scatter, no other option will work``````md
styles:
#solid (default)
#dashed
#dotted
#dashdot
None (idk why this is a thing)``````md
markers:
#.
#,
#o
#v
#^
#<
#>
#1
#2
#3
#4
#5
#s
#p
#*
#h
#H
#+
#x
#D
#d
#_``````md
colors:
#b
#g
#r
#c
#m
#y
#k
#w
#anything from 0-1``````md
fill styles:
#full
#left
#right
#top
#bottom
#none``````md
draw styles:
#steps
#steps-pre
#steps-mid
#steps-post
#default (default)
#gstyles:
#default (default)
#classic
#solarize_light2
#_classic_test
#bmh
#dark_background
#fast
#fivethirtyeight
#ggplot
#grayscale
#seaborn
#seaborn-bright
#seaborn-colorblind
#seaborn-dark
#seaborn-dark-pallette
#seaborn-darkgrid
#seaborn-deep
#seaborn-muted
#seaborn-notebook
#seaborn-paper
#seaborn-pastel
#seaborn-poster
#seaborn-talk
#seaborn-ticks
#seaborn-white
#seaborn-whitegrid
#tableau-colorblind10```
```added: 8/21/2020```"""
    for content in content.split("|"):
        r = 100
        style = "solid"
        marker=color=fillStyle=alpha=makerSize=None
        drawStyle = "default"
        content = Content(content)
        Scatter = False #using points 
        RegScatter = content @ "--scatter" #using the equation
        for op, param in content.opsWithParams():
            if op == "-range": r = int(param)
            elif op == "-lstyle": style = param
            elif op == "-marker": marker = param
            elif op == "-color": color = param
            elif op == "-fillstyle": fillStyle = param
            elif op == "-alpha": alpha = float(param)
            elif op == "-drawstyle": drawStyle = param
            elif op == "-markersize": makerSize = float(param)
            elif op == "-gstyle": 
                matstyle.use(param)
            elif op == "-scatter" and not RegScatter: #makes sure not regular scatter
                Scatter = True
                X = []
                Y = []
                for point in param.split("("):
                    if not point: continue
                    x, y = point.split(",")
                    x = x.strip().strip("(").strip()
                    y = y.strip().strip(")").strip()
                    X.append(x)
                    Y.append(y)
                    try:
                        plt.scatter(X, Y)
                        plt.savefig(f'{msg.author.id}.png')
                    except Exception as e:
                        plt.cla()
                        return await returnMsg(msg, e)
        if not Scatter: #makes sure not using points
            if not content.suitibleForEval():
                return await returnMsg(msg, "nice try")
            equation = content.string.strip()    
            y = [eval(equation.replace("x", str(i)).replace("**", "^").replace("^", "**")) for i in range(r)]
            x = [i + 1 for i in range(len(y))]
            try: 
                if not RegScatter:
                    plt.plot(
                        x, y, 
                        linestyle=style,
                        marker=marker, 
                        color=color,
                        fillstyle=fillStyle,
                        alpha=alpha,
                        drawstyle=drawStyle,
                        markersize=makerSize
                    )
                else:
                    plt.scatter(x, y)
                plt.savefig(f'{str(msg.author.id)}.png')
            except Exception as e:
                plt.cla()
                return await returnMsg(msg, e)
    plt.cla()
    with open(f'{msg.author.id}.png', "rb") as f:
        m = returnMsg(msg, file=discord.File(f, "chart.png"))
    os.remove(f'{msg.author.id}.png')
    matstyle.use("default")
    return await m