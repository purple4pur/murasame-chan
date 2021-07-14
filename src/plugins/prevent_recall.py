from nonebot import on_notice
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import unescape
from nonebot.adapters.cqhttp.event import (
    FriendRecallNoticeEvent,
    GroupRecallNoticeEvent
)


# 私聊防撤回
friend_recall = on_notice()

@friend_recall.handle()
async def handle_friend_recall(bot: Bot, event: FriendRecallNoticeEvent):
    user_id = event.get_user_id()

    # 仅用于自己测试
    if user_id == 593457446:
        msg_id = event.message_id
        msg = await bot.get_msg(message_id=msg_id)
        msg = unescape(msg["raw_message"])
        await bot.send_private_msg(user_id=user_id, message=f"撤回了一条消息：\n{msg}")


test_group_list = [595741581, 873459758]

# 群消息防撤回
group_recall = on_notice()

@group_recall.handle()
async def handle_group_recall(bot: Bot, event: GroupRecallNoticeEvent):
    msg_id = event.message_id
    operator_id = event.operator_id
    sender_id = event.user_id
    group_id = event.group_id

    # 仅供测试
    if not group_id in test_group_list:
        return

    msg = await bot.get_msg(message_id=msg_id)
    msg = unescape(msg["raw_message"])
    if operator_id == sender_id:  # 撤回了自己的消息
        await bot.send_group_msg(group_id=group_id, message=f"({operator_id}) 撤回了：\n{msg}")
    elif sender_id == 2497540344:  # 小丛雨自己的消息被撤回
        await bot.send_group_msg(group_id=group_id, message=f"({operator_id}) 撤回了小丛雨的消息：\n{msg}")
    else:
        await bot.send_group_msg(group_id=group_id, message=f"({operator_id}) 撤回了 ({sender_id}) 的消息：\n{msg}")
