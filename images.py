from common import *

@command
async def rotateImg(msg, content, cmd="rotateImg"):
    """
    rotates an image by an angle, defaults to 90
    required params:
        <img>
    optional params:
        [angle]
    options:
        --nofit: doesn't expand the image to fit the rotation
    aliases:
        rotate
        rotateimg
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    Fit = True if not content @ "--nofit" else False
    if "https://" in content:
        content.replace(url, '')
    if len(content.split(" ")) == 1 and any(content.split(" ")):
        angle = int(content.split(" ")[0])
    else: angle = 90

    if not url: return await returnMsg(msg, "no img provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.rotate(int(angle), expand=Fit)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def mirrorImg(msg, content, cmd="mirrorimg"):
    """
    mirrors an image along y/x axis
    required params:
        <axis (can either by y or x)>
        <img>
    aliases:
        mirror
        mirrorimg
    added: 7/5/2020
    """
    content = Content(content)
    XY = content.split(" ")[0].lower()
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    if XY == "x":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif XY == "y":
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def spreadPixels(msg, content, cmd="spreadpixels"):
    """
    scatters the pixels in an image
    required params:
        <img>
    optional params:
        [dist]: the distance to spread defaults to 100
    aliases:
        spreadpixels
        spreadpx
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    if content.split(" ")[0]:
        dist = int(content.split(" ")[0])
    else: dist = 100
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.effect_spread(dist)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def filterImg(msg, content, cmd="filterimg"):
    """
    filters an image with the filters provided
    required params:
        *<filter(s)>
        <img>
        filters:
        blur
        contour
        detail
        edge_enhance
        edge_enhance_more
        emboss
        find_edges
        sharpen
        smooth
        smooth_more
    added: 7/5/2020
"""
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    if content.split(" ")[0]:
        filt = content.split(" ")[0:]
    else: return await returnMsg(msg, "no filter provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    FILTERS = {
                "blur": lambda: img.filter(ImageFilter.BLUR),
                "contour": lambda: img.filter(ImageFilter.CONTOUR),
                "detail": lambda: img.filter(ImageFilter.DETAIL),
                "edge_enhance": lambda: img.filter(ImageFilter.EDGE_ENHANCE),
                "edge_enhance_more": lambda: img.filter(ImageFilter.EDGE_ENHANCE_MORE),
                "emboss": lambda: img.filter(ImageFilter.EMBOSS),
                "find_edges": lambda: img.filter(ImageFilter.FIND_EDGES),
                "sharpen": lambda: img.filter(ImageFilter.SHARPEN),
                "smooth": lambda: img.filter(ImageFilter.SMOOTH),
                "smooth_more": lambda: img.filter(ImageFilter.SMOOTH_MORE)
            }
    async with msg.channel.typing():
        while filt:
            currFilt = filt[0]
            if not currFilt:
                filt.pop(0)
                continue
            try: img = FILTERS[currFilt]()
            except:
                if currFilt.isnumeric():
                    for x in range(int(currFilt)):
                        FILTERS[lastFilt]()
                else: return await returnMsg(msg, f'Invalid filter: {currFilt}')
            filt.pop(0)
            lastFilt = currFilt
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def pixelColor(msg, content, cmd="pixelcolor"):
    """
    gets the color of a pixel in an image
    required params:
        <x>: x coordinate
        <y>: y coordinate
        <img>
    aliases:
        pxcolor
        pixelcolor
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    if content.split(" ")[0]:
        try: x, y = content.split(" ")
        except: return await returnMsg(msg, "provide x and y")
    else: return await returnMsg(msg, "no coords provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.load()
    r, g, *b = img[int(x), int(y)]
    if len(b) > 1:
        a = b[1]
    else: a = 255
    b = b[0]
    os.remove(filename)
    return await returnMsg(msg, embed=discord.Embed(title=f'R: {r} G: {g} B: {b} ALPHA: {a}', color=discord.Color.from_rgb(r, g, b)))

@command
async def shrinkImg(msg, content, cmd="shrinkimg"):
    """
    reduces the size of an image by a factor
    required params:
        <img>
    optional params:
        [factor]: the factor to shrink by defaults to 2
    aliases:
        shrink
        shrinkimg
    added: 7/5/2020
    """
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    x = content.split(" ")[0]
    if x:
        try:
            red = int(x)
        except:
            return await returnMsg(msg, "must be int")
    else: red = 2
    await saveImg(filename, url)
    img = Image.open(filename)
    img = img.reduce(red)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def colorize(msg, content, cmd="colorize"):
    """
    converts a greyscale img to rgb
    required params:
        <r g b>: the color to convert the blacks to
        <r2 g2 b2>: the color to convert the whites to
    options:
        -mid <r g b>: the color to convert the middle colors to
        -blackpoint <0-255>: the point to consider blacks vs whites
    added: 7/6/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    blackPoint = 0
    whitePoint = 255
    midPoint = 127
    mid = None
    for op, param in content.opsWithParams({"mid": 3}):
        if "-mid" in content:
            mid = tuple(int(x) for x in param)
        if "-midpoint" in content:
            midPoint = int(param[0])
        if "-blackpoint" in content:
            blackPoint = int(param[0])
        if "-whitepoint" in content:
            whitePoint = int(param[0])
    content = content.split(" ", key=lambda x: int(x) if x else False)
    black = content[0:3]
    white = content[3:6]
    await saveImg(filename, url)
    img = Image.open(filename)
    img = ImageOps.colorize(img.convert("L"), black, white, mid=mid, blackpoint=blackPoint, whitepoint=whitePoint, midpoint=midPoint)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def resizeImg(msg, content, cmd="resizeimg"):
    """
    resizes an image
    required params:
        <width>: the width to resize to
        <height>: the height to resize to
        <img>
    optional params:
        [x1 y1 x2 y2]: the part of the image to resize
    aliases:
        resize
        resizeimg
    added: 7/5/2020
    """
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    content = content.split(" ")
    width = content[0]
    height = content[1]
    try:
        width = int(width)
        height = int(height)
        if len(content) > 2 and content[-1]:
            x1 = int(content[2])
            y1 = int(content[3])
            x2 = int(content[4])
            y2 = int(content[5])
    except:
        return await returnMsg(msg, "must be int")
    await saveImg(filename, url)
    img = Image.open(filename)
    try:
        img = img.resize((width, height), box=(x1, y1, x2, y2))
    except:
        img = img.resize((width, height))
    finally:
        img.save(filename)
        with open(filename, "rb") as i:
            await msg.channel.send(file=discord.File(i, filename=filename))
        os.remove(filename)

@command
async def enhanceImg(msg, content, cmd="enhanceimg"):
    """
    similar to filterimg however has different functions
    required params:
        *<method,amnt>: the method, the amount of times (no space after comma)
        <img>
        methods:
        color
        sharpness
        brightness
        contrast
        autocontrast
    aliases:
        enhance
        enhanceimg
    added: 7/5/2020
    """
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    if content.split(" ")[0]:
        enh = content.split(" ")[0:]
    else: return await returnMsg(msg, "no filter provided")
    await saveImg(filename, url)
    img = Image.open(filename)
    async with msg.channel.typing():
        while enh:
            currFilt = enh[0]
            if not currFilt:
                enh.pop(0)
                continue
            try:
                filt = currFilt.split(",")[0]
                amnt = currFilt.split(",")[1]
            except:
                filt = currFilt
                amnt = 1
            try:
                if filt == "autocontrast":
                    img = ImageOps.autocontrast(img.convert("RGB"), cutoff=float(amnt))
                else:
                    i = {
                        "color": ImageEnhance.Color(img),
                        "contrast": ImageEnhance.Contrast(img),
                        "brightness": ImageEnhance.Brightness(img),
                        "sharpness": ImageEnhance.Sharpness(img)
                    }[filt]
                    img = i.enhance(float(amnt))
            except Exception as e:
                print(e)
                return await returnMsg(msg, f'Invalid filter: {filt}')
            enh.pop(0)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def cropImg(msg, content, cmd="crop"):
    """
    crops an image
    required params:
        <img>
    optional params:
        [amnt]: the amount to crop by, defaults to 20
    options:
        -box <x1 y1 x2 y2>
    aliases:
        crop
        cropimg
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    for op, param in content.opsWithParams({"box": 4}):
        if op == "-box":
            x1, y1, x2, y2 = (int(x) for x in param)
            break
    else: amnt = int(content) if content else 20
    await saveImg(filename, url)
    img = Image.open(filename)
    if "-box" in content.opOps:
        img = img.crop(box=(x1, y1, x2, y2))
    else: img = ImageOps.crop(img, border=amnt)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def imgBorder(msg, content, cmd="imgborder"):
    """
    adds a border around an img
    required params:
        <img>
    optional params:
        [px]: the border thickness defaults to 20
        [r g b]: the color of the border
    added: 7/5/2020
    """
    content = content[len(cmd) + 2:].split(" ")
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    if content[0] and len(content) != 3:
        amnt = int(content[0])
    else: amnt = 20
    if len(content) > 1 and len(content) != 3:
        r, g, b = content[1:4]
    elif len(content) == 3:
        r, g, b = content[0:3]
    else: r=g=b = 0
    r = int(r)
    g = int(g)
    b = int(b)
    await saveImg(filename, url)
    img = Image.open(filename)
    img = ImageOps.expand(img, border=amnt, fill=(r, g, b))
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def greyscale(msg, content, cmd="greyscale"):
    """
    converts an image to greyscale
    required params:
        <img>
    aliases:
        greyscale
        grayscale
    added: 7/5/2020
    """
    content = content[len(cmd) + 2:]
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    img = ImageOps.grayscale(img)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def imgNoise(msg, content, cmd="imgnoise"):
    """
    generates some n o i s e 
    required params:
        <width>: the width of the new img
        <height>: the height of the new img
        <stdev>: basically the amount of noise in the form of std deviation
    added: 7/6/2020
    """
    content = content[len(cmd) + 2:]
    filename = f'{msg.author.id}.png'
    width, height = content.split(" ")[0:2]
    stdev = content.split(" ")[2]
    img = Image.new("RGB", (int(width), int(height)))
    img = Image.effect_noise((img.width, img.height), int(stdev))
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def invert(msg, content, cmd="invert"):
    """
    inverts the image
    required params:
        <img>
    optional params:
        [threshold (0-255)]: the point to start inverting from, defaults to 0
    added: 7/5/2020
    """
    content = content[len(cmd) + 2:].split(" ")
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    if content[0].isnumeric():
        amnt = int(content[0])
    else: amnt = 0
    await saveImg(filename, url)
    img = Image.open(filename)
    img = ImageOps.solarize(img.convert("RGB"), threshold=amnt)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def compileImg(msg, content, cmd="compileimg"):
    """
    puts 2 images ontop of each other
    required params:
        <img1 url>
        <img2 url>
        (img 1 goes ontop of img2)
    options:
        -box <x y>: the point where img1 goes on img2
        -alpha <alpha>: the transparency of img1
    aliases:
        compileimg
        combineimg
        addimg
    added: 7/5/2020
    """
    content = Content(content)
    filename1 = f'{msg.author.id}.png'
    filename2 = f'{msg.author.id}2.png'
    await saveImg(filename1, content.split(" ")[0])
    await saveImg(filename2, content.split(" ")[1])
    box = (0, 0)
    alpha = .5
    for op, param in content.opsWithParams({"box": 2}):
        if op == "-box":
            box = tuple(int(x) for x in param)
        elif op == "-alpha":
            alpha = float(param)
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    if "-box" in content.opOps: img1.paste(img2, box=box)
    else: img1 = Image.blend(img1, img2, alpha)
    img1.save(filename1)
    with open(filename1, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename="yes.png"))
    os.remove(filename1)
    os.remove(filename2)

@command
async def imgDiff(msg, content, cmd="imgdiff"):
    """
    finds the difference in 2 images
    required params:
        <img1 url>
        <img2 url>
    added: 7/6/2020
    """
    content = content[len(cmd) + 2:].split(" ")
    filename1 = f'{msg.author.id}.png'
    filename2 = f'{msg.author.id}2.png'
    await saveImg(filename1, content[0])
    await saveImg(filename2, content[1])
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    diffImg = ImageChops.difference(img1.convert("RGB"), img2.convert("RGB"))
    if diffImg.getbbox():
        diffImg.save(filename1)
    with open(filename1, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename="yes.png"))
    os.remove(filename1)
    os.remove(filename2)

@command
async def lightImg(msg, content, cmd="lightimg"):
    """
    makes a new image using the lighter of the 2 pixels for each pixel in the images
    required params:
        <img1 url>
        <img 2 url>
    added: 7/6/2020
    """
    content = content[len(cmd) + 2:].split(" ")
    filename1 = f'{msg.author.id}.png'
    filename2 = f'{msg.author.id}2.png'
    await saveImg(filename1, content[0])
    await saveImg(filename2, content[1])
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    lighterImg = ImageChops.lighter(img1.convert("RGB"), img2.convert("RGB"))
    lighterImg.save(filename1)
    with open(filename1, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename="yes.png"))
    os.remove(filename1)
    os.remove(filename2)

@command
async def darkImg(msg, content, cmd="darkimg"):
    """
    makes a new image using the darker of the 2 pixels for each pixel in the 2 images
    required params:
        <img1 url>
        <img2 url>
    added: 7/6/2020
    """
    content = content[len(cmd) + 2:].split(" ")
    filename1 = f'{msg.author.id}.png'
    filename2 = f'{msg.author.id}2.png'
    await saveImg(filename1, content[0])
    await saveImg(filename2, content[1])
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    darkerImg = ImageChops.darker(img1.convert("RGB"), img2.convert("RGB"))
    darkerImg.save(filename1)
    with open(filename1, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename="yes.png"))
    os.remove(filename1)
    os.remove(filename2)

@command
async def newImg(msg, content, cmd="newimg"):
    """
    creates a new blank image
    optional params:
        [width height]: the width and height of the new img
        [r g b [a]]: the color of the new img
            [a]: the alpha/transparency of the new img
    added: 7/5/2020
    """
    content = content[len(cmd) + 2:].split(" ")
    if "https://" in content:
        content = content.replace(url, '')
    try:
        content[1]
        size = content[0:2]
    except: size = (500, 500)
    if len(content) > 2:
        color = content[2:]
    else: color = [0, 0, 0]
    img = Image.new("RGBA" if len(color) == 4 else "RGB", tuple(int(x) for x in size), tuple(int(x) for x in color))
    img.save(f"{msg.author.id}.png")
    with open(f"{msg.author.id}.png", "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=f"{msg.author.id}.png"))
    os.remove(f"{msg.author.id}.png")

@command
async def rectangle(msg, content, cmd="rectangle"):
    """
    puts a rectangle on an image
    required params:
        <x1 y1 x2 y2>: the coordinates of the rectangle (top left->bottom right)
        <img>
    options:
        -width <px>: the width of the border
        -fill <r g b>: the rgb to fill the rectangle with
        -outline <r g b>: the outline color
        --rgba: if specified provide an alpha for colors
    aliases:
        rectangle
        rect
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    content.calcOps()
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        x1, y1, x2, y2 = content.replace("{width}", str(img.width)).replace("{height}", str(img.height)).string.split(" ")[0:4]
        FR=FG=FB=FA=OA=OR=OG=OB=width = None
        for op, param in content.opsWithParams({"fill": 3, "outline": 3} if not Rgba else {"fill": 4, "outline": 4}):
            if op == "-fill":
                if not Rgba: FR, FG, FB = param
                else: FR, FG, FB, FA = param
            if op == "-outline":
                if not Rgba: OR, OG, OB = param
                else: OR, OG, OB, OA = param
            if op == "-width":
                width = param
        if Rgba:
            draw.rectangle([(int(x1), int(y1)), (int(x2), int(y2))], fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)), outline=None if not OR else (int(OR), int(OG), int(OB), int(OA)), width=1 if not width else int(width))
        else:
            draw.rectangle([(int(x1), int(y1)), (int(x2), int(y2))], fill=None if not FR else (int(FR), int(FG), int(FB)), outline=None if not OR else (int(OR), int(OG), int(OB)), width=1 if not width else int(width))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def imgArc(msg, content, cmd="imgarc"):
    """
    draws an arc on an image
    required params:
        <x1 y1 x2 y2>: the coordinates of the arc (start->end)
        <start angle>: i have no idea just give it
        <end angle>: again i have no idea just give it
        <img>
    options:
        -fill <r g b>: the color of the line
        -width <width>: the width of the line
        --rgba: if specified give alpha for colors
    added: 7/5/2020
    """
    content = Content(content).calcOps()
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        x1, y1, x2, y2 = content.replace("{width}", str(img.width)).replace("{height}", str(img.height)).split(" ")[0:4]
        startAngle = content.split(" ")[4]
        endAngle = content.split(" ")[5]
        FR=FG=FB=FA=width = None
        for op, param in content.opsWithParams({"fill": 3 if not Rgba else 4}):
            if op== "-fill":
                if not Rgba: FR, FG, FB = param
                else: FR, FG, FB, FA = param
            if op == "-width":
                width = param
        if Rgba: draw.arc([(int(x1), int(y1)), (int(x2), int(y2))],
                            startAngle, endAngle,
                            fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)),
                            width=1 if not width else int(width))
        else: draw.arc([(int(x1), int(y1)), (int(x2), int(y2))], int(startAngle), int(endAngle), fill=None if not FR else (int(FR), int(FG), int(FB)), width=1 if not width else int(width))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def ellipse(msg, content, cmd="ellipse"):
    """
    draws a circle/ellipse on an image
    required params:
        <x1 y1 x2 y2>: the coordinates of the ellipse's bounding box (top left->bottom right)
        <img>
    options:
        -fill <r g b>: the color of the circle
        -outline <r g b>: the outline color of the circle
        -width <width>: the width of the line
        --rgba: if specified give alpha for colors
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        x1, y1, x2, y2 = content.replace("{width}", str(img.width)).replace("{height}", str(img.height)).string.split(" ")[0:4]
        FR=FG=FB=FA=OR=OG=OB=OA=width = None
        for op, param in content.opsWithParams({"fill": 3, "outline": 3} if not Rgba else {"fill": 4, "outline": 4}):
            if op == "-fill":
                if not Rgba: FR, FG, FB = param
                else: FR, FG, FB, FA = param
            if "-outline" in params:
                if not Rgba: OR, OG, OB = param
                else: OR, OG, OB, OA = param
            if "-width" in params:
                width = param
        if Rgba: draw.ellipse([(int(x1), int(y1)), (int(x2), int(y2))], outline=None if not OR else (int(OR), int(OG), int(OB), int(OA)), fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)), width=1 if not width else int(width))
        else: draw.ellipse([(int(x1), int(y1)), (int(x2), int(y2))], outline=None if not OR else (int(OR), int(OG), int(OB)), fill=None if not FR else (int(FR), int(FG), int(FB)), width=1 if not width else int(width))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def line(msg, content, cmd="line"):
    """
    draws a line on an image
    required params:
        <x1 y1 x2 y2>: the coordinates of the line (start->end)
        <img>
    options:
        -fill <r g b>: the color of the line
        -width <width>: the width of the line
        --rgba: if specified provide alpha for the colors
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    params = content.split(" ")
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        x1, y1, x2, y2 = content.replace("{width}", str(img.width)).replace("{height}", str(img.height)).string.split(" ")[0:4]
        FR=FG=FB=FA=width = None
        for op, param in content.opsWithParams({"fill": 3 if not Rgba else 4}):
            if "-fill" in params:
                if Rgba: FR, FG, FB, FA = param
                else: FR, FG, FB = param
            if "-width" in params:
                width = param
        if Rgba: draw.line([(int(x1), int(y1)), (int(x2), int(y2))],
                            fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)),
                            width=1 if not width else int(width))
        else: draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=None if not FR else (int(FR), int(FG), int(FB)), width=1 if not width else int(width))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def point(msg, content, cmd="point"):
    """
    makes a point on an image
    required params:
        *<x y>: the coordinates of each point
        <img>: the image to put points on
    options:
        -fill <r g b>: the color of the point
        --rgba: if specified provide an alpha for fill
    aliases:
        point
        imgpoint
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        FR=FG=FB=OR=OG=OB = None
        for op, param in content.opsWithParams({"fill": 3}):
            if op == "-fill":
                FR, FG, FB = param
        newXYS = [""]
        for XY in content.strip().split(" "):
            if len(newXYS[-1]) % 2 != 0:
                newXYS[-1].append(int(XY))
            else:
                newXYS.append([int(XY)])
        XYS = [tuple(XY) for XY in newXYS if type(XY) != str]
        draw.point(XYS, fill=None if not FR else (int(FR), int(FG), int(FB)))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def polygon(msg, content, cmd="poly"):
    """
    draws a polygon on an image
    required params:
        <x1 y1>: the first pair of coordinates
        <x2 y2>: the second pair of coordinates
        <img>: the image to draw on
    optional params:
        *[<x y>]: as many more pairs of coordinates to draw lines to
    options:
        -fill <r g b>: the color of the fill
        -outline <r g b>: the color of the outline
        --rgba: if used provide an alpha for fill and or outline
    aliases:
        poly
        polyg
    added: 7/5/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    await saveImg(filename, url)
    img = Image.open(filename)
    if content @ "--rgba":
        Rgba = True
        img = img.convert("RGBA")
    else: Rgba = False
    img.save(filename)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        FR=FG=FB=FA=OR=OG=OB=OA = None
        for op, param in content.opsWithParams({"fill": 3, "outline": 3} if not Rgba else {"fill": 4, "outline": 4}):
            if op == "-fill":
                if Rgba: FR, FG, FB, FA = param
                else: FR, FG, FB = param
            elif op == "-outline":
                if Rgba: OR, OG, OB, OA = param
                else: OR, OG, OB = param
        XYS = content[0:].split(" ")
        newXYS = [""]
        for XY in XYS:
            if not XY: continue
            if len(newXYS[-1]) % 2 != 0:
                newXYS[-1].append(int(XY))
            else:
                newXYS.append([int(XY)])
        XYS = [tuple(XY) for XY in newXYS if type(XY) != str]
        if Rgba: draw.polygon(XYS, fill=None if not FR else (int(FR), int(FG), int(FB), int(FA)), outline=None if not OR else (int(OR), int(OG), int(OB), int(OA)))
        else: draw.polygon(XYS, fill=None if not FR else (int(FR), int(FG), int(FB)), outline=None if not OR else (int(OR), int(OG), int(OB)))
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def imgText(msg, content, cmd="imgtext"):
    """
    puts text on an image
    required params:
        <x>: the x coordinate, can be number or center/top/bottom
        <y>: the y coordinate
        <text>: the text to put
        <img>: the img to put text on
    options:
        -fill <r g b>: the color of the text
        -font <font name> <font size>: the font and size of the text
            (do help fonts to get a list of fonts)
        -txtwidth <width>: honestly idrk
    added: 7/6/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    await saveImg(filename, url)
    with Image.open(filename) as img:
        draw = ImageDraw.Draw(img)
        split = content.split(" ")
        if split[0] not in ("center", "top", "bottom"):
            x, y = split[0:2]
        else:
            x=y = split[0]
            split.insert(1, "center")
        text = Content(" ".join(split[2:]), removeCmd=False)
        fill=FR=FG=FB=direction=txtWidth = None
        font = ImageFont.load_default()
        if msg.attachments:
            text = text.replace(msg.attachments[0].url, "")
        for op, param in text.opsWithParams({"fill": 3, "font": 2}):
            if op == "-fill":
                FR, FG, FB = param
            if op == "-txtwidth":
                txtWidth = param
            if op == "-font":
                font = f'{param[0].title()}.ttf'
                fontSize = int(param[1])
                font = ImageFont.truetype(f"/usr/share/fonts/truetype/msttcorefonts/{font}", fontSize, encoding="unic")
        imgWidth = img.width
        imgHeight = img.height
        text = text.string
        textWidth, textHeight = font.getsize(text)
        if x == "center":
            draw.text(((imgWidth - textWidth) / 2, (imgHeight - textHeight) / 2), text, font=font, fill=(int(FR), int(FG), int(FB)) if FR else None, stroke_width=0 if not txtWidth else txtWidth)
        elif x == "top":
            draw.text(((imgWidth - textWidth) / 2, 0), text, font=font, fill=(int(FR), int(FG), int(FB)) if FR else None, stroke_width=0 if not txtWidth else txtWidth)
        elif x == "bottom":
            draw.text(((imgWidth - textWidth) / 2, imgHeight - textHeight), text, font=font, fill=(int(FR), int(FG), int(FB)) if FR else None, stroke_width=0 if not txtWidth else txtWidth)
        else:
            draw.text((int(x), int(y)), text, font=font, fill=(int(FR), int(FG), int(FB)) if FR else None, stroke_width=0 if not txtWidth else txtWidth)
        img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def convertImg(msg, content, cmd):
    """
    converts the image to a different mode
    required params:
        <mode>: the mode to convert to
            can be:
            1: pure black and white
            L: greyscale
            refer to https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes for more
    options:
        -palette <palette> (-color <color>): honestly idrk what this does lmao
    added: 7/6/2020
    """
    content = Content(content)
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content.replace(url, '')
    mode = content.split(" ")[0]
    pallete=colors = None
    for op, param in content.opsWithParams():
        if op == "-palette":
            pallete = param
        if op == "-colors":
            colors = param
    await saveImg(filename, url)
    img = Image.open(filename)
    if mode == "LAB":
        return await msg.channel.send("PRAISE L A B ")
    img = img.convert(mode=mode, palette=0 if not pallete else pallete, colors=256 if not colors else colors)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def sortImg(msg, content, cmd="sortimg"):
    """
    sorts image by sort
    required params:
        <sort>: the sorting style
            sort can be:
            wtb: white to black
            r: redmost
            g: greenmost
            b: bluemost
            custom: python expression
                example: px[0] + px[1] will sort by adding red and green values
        <img>: the image to sort
    added: 7/6/2020
    """
    content = content[len(cmd) + 2:].split(" ")
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    sortBy = content[0]
    img = Image.open(filename)
    async with msg.channel.typing():
        data = list(img.getdata())
        if sortBy.lower() in ["btw", "ltd"]:
            data.sort(key=lambda x: sum(x))
        elif sortBy.lower() in ["wtb", "dtl"]:
            data.sort(key=lambda x: sum(x), reverse=True)
        elif sortBy.lower() in ["r", "red"]:
            data.sort(key=lambda x: x[0], reverse=True)
        elif sortBy.lower() in ["g", "green"]:
            data.sort(key=lambda x: x[1], reverse=True)
        elif sortBy.lower() in ["b", "blue"]:
            data.sort(key=lambda x: x[2], reverse=True)
        elif sortBy.lower() == "custom":
            source = " ".join(content[1:])
            if not Content(" ".join(content), removeCmd=False).suitibleForEval():
                return await msg.channel.send("nice try")
            code = compile(source, "", "eval")
            data.sort(key=lambda px: eval(code), reverse=True)
        img.putdata(data)
    img.save(filename)
    with open(filename, "rb") as i:
        await msg.channel.send(file=discord.File(i, filename=filename))
    os.remove(filename)

@command
async def imgBand(msg, content, cmd="imgband"):
    """
    gives a color band of an image
    required params:
        <band (can be r, g, b, or a)>:
            can also be b+g, or g+r etc...
            the color band wanted from the image
    added: 7/6/2020
    """
    content = Content(content)
    content = content.split("+")
    att, filename, url = await getImg(msg)
    if "https://" in content:
        content = content.replace(url, '')
    await saveImg(filename, url)
    bands = [c.strip() for c in content]
    img = Image.open(filename)
    img = img.convert("RGBA")
    r, g, B, a = img.split()
    band = []
    for b in bands:
        if b.strip() == "r": band.append(r)
        elif b.strip() == "g": band.append(g)
        elif b.strip() == 'b': band.append(B)
        elif b.strip() == "a": band.append(a)
    for n, b in enumerate(band):
        b.save(f'{msg.author.id}{n}.png')
    for n, b in enumerate(band):
        with open(f'{msg.author.id}{n}.png', "rb") as i:
            await msg.channel.send(file=discord.File(i, filename=f'{msg.author.id}{n}.png'))
        os.remove(f'{msg.author.id}{n}.png')