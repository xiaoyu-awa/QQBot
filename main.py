# ========= 导入必要模块 ==========
from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.core.notice import NoticeMessage, RequestMessage
from ncatbot.utils import get_log

from src import commands, passiveHandle
from src.timerTask import timerThread, stopThread

# ========== 创建 BotClient ==========
bot = BotClient()
_log = get_log()
# ========= 注册回调函数 ==========
@bot.group_event()
async def on_group_message(msg: GroupMessage):
    _log.info(msg)

    if await passiveHandle.handle(msg):
        return


    if msg.raw_message.startswith("#"):
        await commands.handle(msg)


@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    _log.info(msg)

@bot.notice_event()
async def on_notice(msg: NoticeMessage):
    _log.info(msg)

@bot.request_event()
async def on_request(msg: RequestMessage):
    _log.info(msg)
# ========== 启动 BotClient==========
if __name__ == "__main__":
    timerThread(bot)
    bot.run(bt_uin="2630351717", root="2354934669", enable_webui_interaction=False)
    stopThread()