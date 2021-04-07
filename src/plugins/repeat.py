from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent


repeat = on_message(priority=5, block=False)

@repeat.handle()
async def handle(bot: Bot, event: MessageEvent):
    print(event.get_session_id())
