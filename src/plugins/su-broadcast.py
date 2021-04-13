from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent

from json import loads, dumps


broadcast = on_command("broadcast", aliases={"广播"}, permission=SUPERUSER, priority=1, block=True)

@broadcast.handle()
async def handle(bot: Bot, event: MessageEvent):
    msg = str(event.get_message()).strip()

    groups_data = await bot.get_group_list() # list<dict>
    cnt = 0
    for group in groups_data:
        gid = group["group_id"]
        await bot.send_group_msg(group_id=gid, message=msg)
        cnt += 1

    await broadcast.finish(f"已经发送给共 {cnt} 个群。")
