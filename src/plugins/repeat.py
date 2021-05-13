from nonebot import on_message
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent
from nonebot.adapters.cqhttp.permission import GROUP


# {群号: [最后一条消息内容, 已被复读次数, 是否已经被我复读]}
history = {}

# 只响应来自群聊的消息
repeat = on_message(permission=GROUP, priority=5, block=False)

@repeat.handle()
async def handle(bot: Bot, event: MessageEvent):
    session_id = event.get_session_id().split("_")
    group_id = session_id[1]
    msg = event.get_message()

    # 该群被记录过
    if group_id in history:

        # 群友开始复读了
        if msg == history[group_id][0]:
            history[group_id][1] += 1

            # 已经被群友复读了超过 2 次，我来复读
            if history[group_id][1] >= 2 and history[group_id][2] is False:
                await repeat.send(msg)
                history[group_id][2] = True

        # 更新最后一条消息记录
        else:
            history[group_id] = [msg, 1, False]

    # 该群还未被记录
    else:
        history[group_id] = [msg, 1, False]
