import asyncio
import datetime
import threading
import time

from ncatbot.core import BotClient
from functools import wraps
from threading import Thread
from typing import Callable, Optional

from schedule import every, repeat, run_pending

from src.utils import setGaoKaoWithBot

stop = False
bot = None

def threaded(name: Optional[str] = None, daemon: bool = False):
    """
    多线程装饰器，被装饰的函数将在独立线程中运行
    :param name: 线程名称(默认使用函数名称)
    :param daemon: 是否设置为守护线程
    """
    def decorator(func: Callable):
        thread_name = name or func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs) -> Thread:
            """
            包装函数，创建并启动线程
            返回线程对象以便后续控制
            """
            # 创建线程对象
            thread = Thread(
                target=func,
                name=thread_name,
                args=args,
                kwargs=kwargs,
                daemon=daemon
            )
            # 启动线程
            thread.start()
            # 返回线程对象以便后续操作（如 join）
            return thread
        return wrapper
    return decorator

def timerThread(_bot: BotClient):
    global bot
    bot = _bot

    stopThread()
    repeatThread()
    return

@threaded(name="stop")
def stopThread():
    global stop
    while True:
        if threading.main_thread().is_alive():
            pass
        else:
            stop = True
            break

@threaded(name="repeat")
def repeatThread():
    while True:
        global stop
        if stop:
            break
        run_pending()
        time.sleep(1)

@repeat(every().day.at("00:00"))
def gaoKao():
    global bot
    asyncio.run(setGaoKaoWithBot(bot))



"""
@repeat(every(15).seconds)
def poke():
    global bot
    print("test")
    asyncio.run(bot.api.send_poke(user_id=2354934669, group_id=679198724))
    asyncio.run(bot.api.post_group_msg(group_id=981268335, text="test"))
"""