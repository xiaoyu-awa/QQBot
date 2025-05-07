from ncatbot.core import GroupMessage, MessageChain, Image
from psutil import *


async def replyMessage(message: GroupMessage, content):
    await message.reply(content)
    await changeGroupNick(message)


async def sendMessage(message: GroupMessage, content):
    await message.api.post_group_msg(group_id=message.group_id, text=content)
    await changeGroupNick(message)


async def replyLocalPicMessage(message, content, pic):
    msg = MessageChain([
        content,
        Image(pic)
    ])
    await message.api.post_group_msg(group_id=message.group_id, rtf=msg)
    await changeGroupNick(message)


async def replyWebPicMessage(message, content, file_url):
    msg = MessageChain([
        content,
        Image(file_url)
    ])
    await message.api.post_group_msg(group_id=message.group_id, rtf=msg)
    await changeGroupNick(message)


async def changeGroupNick(message: GroupMessage):
    await message.api.set_group_card(group_id=message.group_id, user_id=message.self_id,
                                     card="团子呐 | 大脑负载:" + str(cpu_percent(interval=2)) + "%")
