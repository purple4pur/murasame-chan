from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageSegment

from pathlib import Path
from random import choice


records_sleep = ["你怎么睡得着的.mp3", "上课不要睡觉.mp3"]
records_rest = ["三点.acc", "七点.acc"]

# 得到当前文件绝对路径
path = Path(__file__).parent.absolute()


def get_record_url(obj: str):
    # 随机返回一段录音路径
    if obj is "sleep":
        return f"file://{path}/../static/audio/{choice(records_sleep)}"
    elif obj is "rest":
        return f"file://{path}/../static/audio/{choice(records_rest)}"


sleep = on_command("sleep", priority=3, block=True)

@sleep.handle()
async def handle_sleep(bot: Bot):
    await sleep.finish(MessageSegment.record(get_record_url("sleep")))


rest = on_command("rest", aliases={"下班"}, priority=3, block=True)

@rest.handle()
async def handle_rest(bot: Bot):
    await rest.finish(MessageSegment.record(get_record_url("rest")))
