from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageSegment

from pathlib import Path
from random import choice


records = ["你怎么睡得着的.mp3", "上课不要睡觉.mp3"]

# 得到当前文件绝对路径
path = Path(__file__).parent.absolute()

def get_record_url():
    # 随机返回一段录音路径
    return f"file://{path}/../static/audio/{choice(records)}"


sleep = on_command("sleep", priority=3, block=True)

@sleep.handle()
async def handle_en(bot: Bot):
    await sleep.finish(MessageSegment.record(get_record_url()))
