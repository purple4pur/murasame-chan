from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent

from json import loads, dumps


status = on_command("status", permission=SUPERUSER, priority=1, block=True)

@status.handle()
async def handle(bot: Bot, event: MessageEvent):
    json = await bot.get_friend_list()
    json_str = dumps(json)
    await status.send(json_str)
