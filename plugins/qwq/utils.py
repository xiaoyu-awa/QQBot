import datetime

from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse
from ncatbot.core import GroupMessage, BotClient

from . import picHandle


async def getMCServerStatus(mc_host, mc_port) -> JavaStatusResponse:
    offline = False
    try:
        server = JavaServer.lookup(f"{mc_host}:{mc_port}")
    except (TimeoutError, ConnectionRefusedError):
        offline = True
    if not offline:
        return server.status()


async def setGaoKao(message: GroupMessage):
    date1 = datetime.date.today()
    date2 = datetime.date(2025, 6, 7)
    delta = date2 - date1
    days = delta.days

    picHandle.getGaoKaoPic(days)
    await message.api.set_group_name(679198724, "高考倒计时: " + str(days) + "天")
    await message.api.set_group_portrait(679198724, "pic/temp/GaoKao.png")


async def isAdmin(message: GroupMessage):
    info = await message.api.get_group_member_info(message.group_id, message.user_id, False)
    if info["data"]["role"] == "admin" or info["data"]["role"] == "owner":
        return True
    return False
