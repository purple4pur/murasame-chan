from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment

from datetime import datetime


contact = on_command("contact", aliases={"feedback"}, priority=1, block=True)

@contact.handle()
async def handle(bot: Bot, event: MessageEvent):
    is_from_private = True
    session_id = event.get_session_id().split("_")
    if len(session_id) == 3:
        is_from_private = False
        group_id = session_id[1]
    
    content = str(event.get_message()).strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if is_from_private:
        msg = f"[Contact Message]\nSender: {event.get_user_id()}\nFrom: Private\nTime: {now}\nContent: {content}"
    else:
        msg = f"[Contact Message]\nSender: {event.get_user_id()}\nFrom: Group({group_id})\nTime: {now}\nContent: {content}"
    await bot.send_private_msg(user_id=593457446, message=msg)

    await contact.finish("小从雨已经向狗修金报告啦~")
