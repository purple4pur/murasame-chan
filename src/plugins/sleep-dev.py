from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageSegment

from os.path import dirname, abspath


sleep = on_command("sleep", priority=1, block=True)

@sleep.handle()
async def handle(bot: Bot):
    path = dirname(abspath(__file__))
    await sleep.finish(MessageSegment.record(f"file:///{path}\\..\\static\\audio\\你怎么睡得着的.mp3"))
