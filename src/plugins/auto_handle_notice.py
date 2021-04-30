from nonebot import on_notice, on_request
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageSegment, unescape
from nonebot.adapters.cqhttp.event import (
    FriendRequestEvent,
    FriendAddNoticeEvent,
    GroupRequestEvent,
    FriendRecallNoticeEvent,
    GroupRecallNoticeEvent
)


welcome_msg = "ムラサメです！请到 purple4pur.com/murasame-chan 查看小丛雨的使用帮助哦！"


# 加好友请求
friend_request = on_request()

@friend_request.handle()
async def handle(bot: Bot, event: FriendRequestEvent):
    await event.approve(bot)


# 新好友通知
friend_add = on_notice()

@friend_add.handle()
async def handle(bot: Bot, event: FriendAddNoticeEvent):
    user_id = event.user_id
    await bot.send_private_msg(user_id=user_id, message=welcome_msg)
    await bot.send_private_msg(user_id=593457446, message=f"已添加新好友：{user_id}")


# 加群邀请
group_request = on_notice()

@group_request.handle()
async def handle(bot: Bot, event: GroupRequestEvent):
    await event.approve(bot)
    group_id = event.group_id
    await bot.send_group_msg(group_id=group_id, message=welcome_msg)
    await bot.send_private_msg(user_id=593457446, message=f"已加入新群聊：{group_id}")


# 私聊防撤回
friend_recall = on_notice()

@friend_recall.handle()
async def handle(bot: Bot, event: FriendRecallNoticeEvent):
    msg_id = event.message_id
    user_id = event.get_user_id()
    msg = await bot.get_msg(message_id=msg_id)
    msg = unescape(msg["raw_message"])
    await bot.send_private_msg(user_id=user_id, message=f"撤回了一条消息：\n{msg}")


test_group_list = [595741581, 873459758]

# 群消息防撤回
group_recall = on_notice()

@group_recall.handle()
async def handle(bot: Bot, event: GroupRecallNoticeEvent):
    msg_id = event.message_id
    operator_id = event.operator_id
    sender_id = event.user_id
    group_id = event.group_id

    # 仅供测试
    if not group_id in test_group_list:
        return

    msg = await bot.get_msg(message_id=msg_id)
    msg = unescape(msg["raw_message"])
    if operator_id == sender_id:
        await bot.send_group_msg(group_id=group_id, message=f"({operator_id}) 撤回了：\n{msg}")
    elif sender_id == 2497540344:
        await bot.send_group_msg(group_id=group_id, message=f"({operator_id}) 撤回了小丛雨的消息：\n{msg}")
    else:
        await bot.send_group_msg(group_id=group_id, message=f"({operator_id}) 撤回了 ({sender_id}) 的消息：\n{msg}")
