from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent


status = on_command("status", permission=SUPERUSER, priority=1, block=True)

@status.handle()
async def handle(bot: Bot, event: MessageEvent):
    friends_data = await bot.get_friend_list() # list
    num_friends = len(friends_data) - 2        # 排除自己和 babyQ

    groups_data = await bot.get_group_list()
    num_groups = len(groups_data)

    await status.finish(f"当前共 {num_friends} 个好友，{num_groups} 个群组。")
