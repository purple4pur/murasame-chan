from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent

from json import loads, dumps


broadcast = on_command("broadcast", aliases={"广播"}, permission=SUPERUSER, priority=1, block=True)

@broadcast.handle()
async def handle(bot: Bot, event: MessageEvent):
    msg = str(event.get_message()).strip()

    groups_data = await bot.get_group_list() # list
    print(type(groups_data))
    print(groups_data[0])

    # await broadcast.finish()
