from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment


contact = on_command("contact", aliases={"feedback"}, priority=1, block=True)

@contact.handle()
async def handle(bot: Bot, event: MessageEvent):
    msg = str(event.get_message()).strip()
    bot.send_private_msg(user_id=593457446, message=msg)
