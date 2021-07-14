from nonebot import on_notice, on_request
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp.event import (
    FriendRequestEvent,
    FriendAddNoticeEvent,
    GroupRequestEvent
)


welcome_msg = "ムラサメです！请到 purple4pur.com/murasame-chan 查看小丛雨的使用帮助哦！"


# 加好友请求
friend_request = on_request()

@friend_request.handle()
async def handle_friend_request(bot: Bot, event: FriendRequestEvent):
    await event.approve(bot)


# 新好友通知
friend_add = on_notice()

@friend_add.handle()
async def handle_friend_add(bot: Bot, event: FriendAddNoticeEvent):
    user_id = event.user_id
    await bot.send_private_msg(user_id=user_id, message=welcome_msg)
    await bot.send_private_msg(user_id=593457446, message=f"已添加新好友：{user_id}")


# 加群邀请
group_request = on_notice()

@group_request.handle()
async def handle_group_request(bot: Bot, event: GroupRequestEvent):
    await event.approve(bot)
    group_id = event.group_id
    await bot.send_group_msg(group_id=group_id, message=welcome_msg)
    await bot.send_private_msg(user_id=593457446, message=f"已加入新群聊：{group_id}")
