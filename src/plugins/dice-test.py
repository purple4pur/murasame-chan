from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment

dice = on_command("dice", priority=1, block=True)

@dice.handle
async def handle(bot: Bot, event: Event, state: T_State):
    await dice.finish(MessageSegment.dice())
