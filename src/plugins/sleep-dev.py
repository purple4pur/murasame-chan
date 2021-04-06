from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageSegment


sleep = on_command("sleep", priority=1, block=True)

@sleep.handle()
async def handle(bot: Bot):
    await sleep.finish(MessageSegment.record("..\\static\\audio\\你怎么睡得着的.mp3"))
