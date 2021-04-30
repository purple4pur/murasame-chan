from nonebot import on_request
from nonebot import on_notice
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp.event import FriendRequestEvent, FriendAddNoticeEvent, FriendRecallNoticeEvent


friend_add = on_notice()

@friend_add.handle()
async def handle(bot: Bot, event: FriendAddNoticeEvent):
    print(event)


friend_recall = on_notice()

@friend_recall.handle()
async def handle(bot: Bot, event: FriendRecallNoticeEvent):
    print(event)
