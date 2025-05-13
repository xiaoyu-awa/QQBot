import re
from functools import wraps
from typing import Dict, Tuple, Callable, List

from ncatbot.core import GroupMessage

from src import messageUtils, utils
from .config.configUtils import sensitive_word
from .config.groupConfig import GroupConfig, GroupConfigItem


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


def passive(name: str = None):
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


'''
被动消息处理函数
@passive 只能精准检测
:return 返回值为true时，消息将不会继续传递
'''


async def handle(message: GroupMessage):
    if await muteByKeyWord(message):
        return True

    passiveMsg, msg = CommandSystem.parse_input(message)
    await CommandSystem.handle_command(passiveMsg, msg)

    return False


async def muteByKeyWord(message: GroupMessage):
    if await utils.isAdmin(message):
        return
    groupSettings = GroupConfig(message.group_id)
    if not groupSettings.getConfigByEnum(groupSettings.config_map[GroupConfigItem.KEYWORD_MUTE.key]):
        return False
    content = ""
    for i in message.message:
        if i["type"] != "text":
            continue
        else:
            content += i["data"]["text"]
    content = content.replace(" ", "")
    for i in groupSettings.getConfigByEnum(groupSettings.config_map[GroupConfigItem.KEYWORDS.key]) + sensitive_word.get(
            "sensitive", []):
        result_match = re.search(i, content)
        if result_match:
            await message.api.delete_msg(message.message_id)
            await message.api.set_group_ban(message.group_id, message.user_id, 10)
            await messageUtils.sendMessage(message, "不要发怪东西嗷")
            return True
    return False


@passive("叫妈妈")
async def mom(message: GroupMessage):
    if message.user_id == 3510936741:
        await messageUtils.replyMessage(message, "妈妈")
    return


@passive("test")
async def test(message: GroupMessage):
    if message.user_id == 2354934669:
        await messageUtils.replyMessage(message, "test")
    return
