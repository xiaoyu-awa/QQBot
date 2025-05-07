from mcstatus.status_response import JavaStatusResponse
from PIL import ImageFont, ImageDraw, Image
import base64

color_codes = {
        '0': (00,00,00),  # 黑色
        '1': (00,00,0xAA),  # 深蓝
        '2': (00,0xAA,00),  # 深绿
        '3': (00,0xAA,0xAA),  # 青色
        '4': (0xAA,00,00),  # 深红
        '5': (0xAA,00,0xAA),  # 紫色
        '6': (0xFF,0xAA,00),  # 金色
        '7': (0xAA,0xAA,0xAA),  # 灰色
        '8': (55,55,55),  # 深灰
        '9': (55,55,0xFF),  # 蓝色
        'a': (55,0xFF,55),  # 绿色
        'b': (55,0xFF,0xFF),  # 浅蓝
        'c': (0xFF,55,55),  # 红色
        'd': (0xFF,55,0xFF),  # 粉色
        'e': (0xFF,0xFF,55),  # 黄色
        'f': (0xFF,0xFF,0xFF)  # 白色
    }
def getMCServerIcon(status : JavaStatusResponse):
    font = ImageFont.truetype("assets/minecraft.ttf", 12)
    #获取服务器图标
    base64_str = status.icon
    head, context = base64_str.split(",")
    img_data = base64.b64decode(context)
    with open("pic/temp/mcServerIcon.png", "wb") as f:
        f.write(img_data)
    #打开底片
    base = Image.open("pic/mcServer.png")
    #粘贴服务器图标
    box = (6, 4, 70, 68)
    icon = Image.open("pic/temp/mcServerIcon.png")
    base.paste(icon, box)

    #获取服务器介绍
    motd = (status.motd.to_minecraft().replace("§l", "")
            .replace("§k", "")
            .replace("§m", "")
            .replace("§n", "")
            .replace("§o", "")
            .replace("§r", "")
            .replace("§", "§!@!"))
    #切割文字位置
    box = (76, 28, 550, 62)
    textPic = base.crop(box)
    #绘制文字
    draw = ImageDraw.Draw(textPic)
    x,y=0,0
    color = (0,0,0)
    for txt in motd.split("§"):
        if txt == "":
            continue
        rep = ""
        if (txt[0]+txt[1]+txt[2]+txt[3]) in {"!@!0","!@!1","!@!2","!@!3","!@!4","!@!5","!@!6","!@!7","!@!8","!@!9","!@!a","!@!b","!@!c","!@!d","!@!e","!@!f"}:
            color = color_codes.get((txt[0]+txt[1]+txt[2]+txt[3]).replace("!@!",""))
            rep = txt[0]+txt[1]+txt[2]+txt[3]
        else:
            color = (255,255,255)
        txt = txt.replace(rep,"")
        draw.text((x, y), txt, color, font=font)
        last_x = x
        for i in txt:
            if i == " ":
                x+=4
            else:
                x+=8
        if len(txt.split("\n"))==2:
            y+=22
            x=0
            last_x=0
    #结束绘制
    base.paste(textPic, box)

    #绘制玩家数量
    box = (400, 8, 580, 20)
    textPic = base.crop(box)
    draw = ImageDraw.Draw(textPic)
    x=580-400
    text = "".join(reversed(f"{status.players.online}/{status.players.max}"))
    for i in text:
        x -= 8
        draw.text((x, 0), i, (255,255,255), font=font)
    #结束绘制
    base.paste(textPic, box)

    return base
def getGaoKaoPic(day):
    font_s = ImageFont.truetype("assets/minecraft.ttf", 60)
    font_b = ImageFont.truetype("assets/minecraft.ttf", 110)
    image = Image.new('RGB', (600, 600), (0x55, 0x55, 0x55))

    draw = ImageDraw.Draw(image)
    draw.text((120,180), "距离高考还剩", (0xff,0xff,0xff), font=font_s)
    draw.text((170,300), str(day) + "天", (0xff,00,00), font=font_b)

    image.save("pic/temp/GaoKao.png")