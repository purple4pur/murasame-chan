from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageSegment

from pathlib import Path
from random import choice


path = Path(__file__).parent.absolute()
records = ["你怎么睡得着的.mp3", "上课不要睡觉.mp3"]


sleep_en = on_command("sleep", priority=3, block=True)
sleep_zh = on_command("睡觉", priority=3, block=True)

@sleep_en.handle()
async def handle_en(bot: Bot):
    await sleep_en.finish(MessageSegment.record(get_record_url()))

@sleep_zh.handle()
async def handle_zh(bot: Bot):
    await sleep_zh.finish(MessageSegment.record(get_record_url()))


def get_record_url():
    return f"file://{path}/../static/audio/{choice(records)}"
