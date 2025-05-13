# ========= 导入必要模块 ==========
from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.core.notice import NoticeMessage, RequestMessage
from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.utils import get_log

from . import commands, passiveHandle, timerTask

bot = CompatibleEnrollment
_log = get_log()

class qwq(BasePlugin):
    name = "qwq"  # 插件名称
    version = "0.0.1"  # 插件版本

    async def on_load(self):
        _log.info("插件加载成功！")
        await timerTask.init(self)

    @bot.group_event()
    async def on_group_message(self, msg: GroupMessage):
        _log.info(msg)

        if await passiveHandle.handle(msg):
            return

        if msg.raw_message.startswith("#"):
            await commands.handle(msg)

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):
        _log.info(msg)

    @bot.notice_event()
    async def on_notice(self, msg: NoticeMessage):
        _log.info(msg)

    @bot.request_event()
    async def on_request(self, msg: RequestMessage):
        _log.info(msg)
