from nonebot import on_notice
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp.event import (
    FriendRequestEvent,
    GroupRequestEvent,
    FriendRecallNoticeEvent,
    GroupRecallNoticeEvent
)


# 加好友请求
friend_request = on_notice()

@friend_request.handle()
async def handle(bot: Bot, event: FriendRequestEvent):
    await event.approve(bot)
    user_id = event.user_id
    await bot.send_private_msg(user_id=user_id, message="ムラサメです！前往 purple4pur.com/murasame-chan 查看小丛雨的使用帮助哦！")
    await bot.send_private_msg(user_id=593457446, message=f"已添加新好友：{user_id}")


# 加群邀请
group_request = on_notice()

@group_request.handle()
async def handle(bot: Bot, event: GroupRequestEvent):
    await event.approve(bot)
    group_id = event.group_id
    await bot.send_group_msg(group_id=group_id, message="ムラサメです！请到 purple4pur.com/murasame-chan 查看小丛雨的使用帮助哦！")
    await bot.send_private_msg(user_id=593457446, message=f"已加入新群聊：{group_id}")


# 私聊防撤回
friend_recall = on_notice()

@friend_recall.handle()
async def handle(bot: Bot, event: FriendRecallNoticeEvent):
    msg_id = event.message_id
    user_id = event.get_user_id()
    msg = await bot.get_msg(message_id=msg_id)
    msg = msg["message"]
    await bot.send_private_msg(user_id=user_id, message=f"撤回了一条消息：\n{msg}")


# 群消息防撤回
group_recall = on_notice()

@group_recall.handle()
async def handle(bot: Bot, event: GroupRecallNoticeEvent):
    msg_id = event.message_id
    operator_id = event.operator_id
    sender_id = event.user_id
    group_id = event.group_id

    # 测试
    if group_id != 873459758:
        return

    msg = await bot.get_msg(message_id=msg_id)
    msg = msg["message"]
    await bot.send_group_msg(group_id=group_id, message=f"({operator_id}) 撤回了 ({sender_id}) 的消息：\n{msg}")
