from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment

from datetime import datetime


contact = on_command("contact", aliases={"feedback"}, priority=1, block=True)

@contact.handle()
async def handle(bot: Bot, event: MessageEvent):
    content = str(event.get_message()).strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"Sender: {event.get_user_id()}\nTime: {now}\nContent: {content}"
    await bot.send_private_msg(user_id=593457446, message=msg)

    await contact.finish("小从雨已经向狗修金报告啦~")
