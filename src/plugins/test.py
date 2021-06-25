from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment, unescape

test = on_command("test", priority=1, block=True)

@test.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    await test.finish(MessageSegment.image("https://t.ly/Syi3"))
