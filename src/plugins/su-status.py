from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent

from json import loads, dumps


status = on_command("status", permission=SUPERUSER, priority=1, block=True)

@status.handle()
async def handle(bot: Bot, event: MessageEvent):
    friends_data = await bot.get_friend_list()
    friends = loads(friends_data)
    num_friends = len(friends) - 2

    groups_data = await bot.get_group_list()
    groups = loads(groups_data)
    num_groups = len(groups)

    print(dumps(groups_data))

    await status.finish(f"当前共 {num_friends} 个好友，{num_groups} 个群组。")
