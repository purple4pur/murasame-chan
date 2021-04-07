from nonebot import on_message
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent


# {群号: [最后一条消息内容, 已被复读次数, 是否已经被我复读]}
history = {}

repeat = on_message(priority=5, block=False)

@repeat.handle()
async def handle(bot: Bot, event: MessageEvent):
    session_id = event.get_session_id().split("_")
    if len(session_id) == 3:
        group_id = session_id[1]
        msg = event.get_message()
        if group_id in history:
            if msg == history[group_id][0]:
                history[group_id][1] += 1
        else:
            history[group_id] = [msg, 1, False]
        print(history)
