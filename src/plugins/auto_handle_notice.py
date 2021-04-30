from nonebot import on_request
from nonebot import on_notice
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp.event import FriendRequestEvent, FriendAddNoticeEvent, FriendRecallNoticeEvent


# friend_add = on_notice()

# @friend_add.handle()
# async def handle(bot: Bot, event: FriendRequestEvent):
#     await event.approve(bot)


friend_recall = on_notice()

@friend_recall.handle()
async def handle(bot: Bot, event: FriendRecallNoticeEvent):
    print(event.message_id)
    msg_id = event.message_id
    msg = await bot.get_msg(message_id=msg_id)
    print(msg)
    await bot.send(event, msg)

