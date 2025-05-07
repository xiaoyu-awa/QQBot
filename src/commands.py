from functools import wraps
from typing import Dict, List, Tuple, Callable

from ncatbot.core import GroupMessage

from . import messageUtils, configUtils, groupConfig
from . import picHandle
from . import utils
from .groupConfig import GroupConfig, ConfigItem
from .utils import isAdmin
from .configUtils import config, sensitive_word


class Command:
    registry: Dict[str, 'Command'] = {}

    def __init_subclass__(cls, name: str = None):
        command_name = name or cls.__name__.lower()
        cls.registry[command_name] = cls

    @classmethod
    def execute(cls, msg: GroupMessage):
        raise NotImplementedError
class CommandSystem:
    @staticmethod
    def parse_input(msg: GroupMessage) -> Tuple[str, GroupMessage]:
        parts = msg.raw_message.split()[0]
        if not parts:
            return "", msg
        return parts, msg

    @classmethod
    async def handle_command(cls, command_name: str, msg: GroupMessage):
        handler = Command.registry.get(command_name)
        if not handler:
            return
        if isinstance(handler, type) and issubclass(handler, Command):
            await handler.execute(msg)
        elif callable(handler):
            await handler(msg)
        else:
            return
def command(name: str = None):
    def decorator(func: Callable):
        cmd_name = name or func.__name__

        @wraps(func)
        def wrapper(args: List[str]):
            try:
                return func(args)
            except Exception as e:
                return

        Command.registry[cmd_name] = wrapper
        return wrapper

    return decorator
def admin(func: Callable):
    @wraps(func)
    async def wrapper(message: GroupMessage, *args, **kwargs):
        if not await isAdmin(message):
            await messageUtils.replyMessage(message, "?")
            return
        return await func(message, *args, **kwargs)

    return wrapper

async def handle(message: GroupMessage):
    cmd_name, msg = CommandSystem.parse_input(message)
    await CommandSystem.handle_command(cmd_name, msg)


"""
画个分界线好看x=========================================================================================
"""


@command(name="#获取服务器状态")
async def getMCServerStatus(message: GroupMessage):
    if len(message.raw_message.split()) == 1:
        await messageUtils.replyMessage(message,
                                        "请输入正确的命令格式，例如：#获取服务器状态 [host] {port}")
    elif len(message.raw_message.split()) == 2 or len(message.raw_message.split()) == 3:
        port = 25565
        host = message.raw_message.split()[1]
        if len(message.raw_message.split()) == 2:
            if len(message.raw_message.split()[1].split(":")) == 2:
                host = message.raw_message.split()[1].split(":")[0]
                port = message.raw_message.split()[1].split(":")[1]
        if len(message.raw_message.split()) == 3:
            host = message.raw_message.split()[1]
            port = message.raw_message.split()[2]

        ser = await utils.getMCServerStatus(host, port)
        picHandle.getMCServerIcon(ser).save("pic/temp/mcServerInfo.png")
        players = "在线玩家：| "
        if not (ser.players.sample is None):
            for i in ser.players.sample:
                players += i.name + " | "
            if players == "在线玩家：| ":
                players = ""
        else:
            players = ""

        await messageUtils.replyLocalPicMessage(message, players, "pic/temp/mcServerInfo.png")
    return

@command(name="#菜单")
async def menu(message: GroupMessage):
    await messageUtils.replyMessage(message, "菜单:\n")
    return

@command(name="#随机图片")
async def randomPic(message: GroupMessage):
    groupSettings = GroupConfig(config,message.group_id)
    if not groupSettings.getConfigByEnum(groupSettings.config_map[ConfigItem.RANDOMPIC.key]):
        await messageUtils.sendMessage(message, "功能已禁用")
        return
    await messageUtils.replyWebPicMessage(message, "", "https://www.loliapi.com/acg/index.php")
    return


"""
虽然有admin装饰器 但是画个分界线好看x=========================================================================================
"""


@command(name="#高考")
@admin
async def gaoKao(message: GroupMessage):
    if message.group_id == 679198724:
        await utils.setGaoKao(message)
    return


@command(name="#禁言")
@admin
async def mute(message: GroupMessage):
    if len(message.raw_message.split()) == 1:
        await messageUtils.replyMessage(message,
                                        "请输入正确的命令格式，例如：#禁言 [qq/@at] {time（秒)}")
        return
    if len(message.raw_message.split()) == 2:
        if len(message.message) == 2:
            await message.api.set_group_ban(message.group_id, message.message[1]["data"]["qq"], 60)
        else:
            await message.api.set_group_ban(message.group_id, message.raw_message.split()[1], 60)
        return
    if len(message.raw_message.split()) == 3:
        if len(message.message) == 3:
            await message.api.set_group_ban(message.group_id, message.message[1]["data"]["qq"],
                                            int(message.raw_message.split()[2]))
        else:
            await message.api.set_group_ban(message.group_id, message.raw_message.split()[1],
                                            int(message.raw_message.split()[2]))
        return


@command(name="#群设置")
@admin
async def showGroupSettings(message: GroupMessage):
    s = ""
    groupSettings = GroupConfig(config,message.group_id)
    for i in groupSettings.listAllConfigItems().keys():
        s += i.cn_name + ": " + str(groupSettings.getConfigByEnum(groupSettings.config_map[i.key])) + "\n"
    await messageUtils.replyMessage(message, s)
    return


@command(name="#关键词屏蔽")
@admin
async def showGroupSettings(message: GroupMessage):
    groupSettings = GroupConfig(config,message.group_id)
    if not groupSettings.getConfigByEnum(groupSettings.config_map[ConfigItem.KEYWORD_MUTE.key]):
        groupSettings.setConfigByEnum(groupSettings.config_map[ConfigItem.KEYWORD_MUTE.key], True)
        await reloadSettings(message)
        await messageUtils.replyMessage(message, "关键词屏蔽:开")
    else:
        groupSettings.setConfigByEnum(groupSettings.config_map[ConfigItem.KEYWORD_MUTE.key], False)
        await reloadSettings(message)
        await messageUtils.replyMessage(message, "关键词屏蔽:关")
    return

@command(name="#重载配置文件")
@admin
async def reloadSettings(message: GroupMessage):
    config.load()
    sensitive_word.load()


@command("#test")
@admin
async def test(message: GroupMessage):
    return
