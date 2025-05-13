import datetime

from ncatbot.utils import get_log

from . import picHandle

_log = get_log("定时任务")
scheduled_tasks = {}


def scheduled_task(name, interval=None, conditions=None, max_runs=None, args=None, kwargs=None, args_provider=None, kwargs_provider=None):
    def decorator(func):
        # 检查 name 是否重复
        if name in scheduled_tasks:
            raise ValueError(f"定时任务名称 '{name}' 已经存在")

        scheduled_tasks[name] = {
            'func': func,
            'interval': interval,
            'conditions': conditions,
            'max_runs': max_runs,
            'args': args,
            'kwargs': kwargs,
            'args_provider': args_provider,
            'kwargs_provider': kwargs_provider,
        }

    return decorator


async def init(plugin):
    for name, task_info in scheduled_tasks.items():
        ret = plugin.add_scheduled_task(job_func=task_info["func"], name=name, interval=task_info["interval"],
                                  conditions=task_info["conditions"], max_runs=task_info["max_runs"],
                                  args=task_info["args"], kwargs=task_info["kwargs"],
                                  args_provider=task_info["args_provider"],
                                  kwargs_provider=task_info["kwargs_provider"], )
        if ret:
            _log.info(f"定时任务 '{name}' 已注册")
        else:
            _log.error(f"定时任务 '{name}' 注册失败")


@scheduled_task(name="高考倒计时", interval="00:00")
async def gaoKao(plugin):
    date1 = datetime.date.today()
    date2 = datetime.date(2025, 6, 7)
    delta = date2 - date1
    days = delta.days

    picHandle.getGaoKaoPic(days)
    await plugin.api.set_group_name(679198724, "高考倒计时: " + str(days) + "天")
    await plugin.api.set_group_portrait(679198724, "pic/temp/GaoKao.png")
