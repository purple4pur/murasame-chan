from nonebot import on_command
from nonebot.rule import keyword
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from random import randint


test = on_command(rule=keyword("不"), priority=2, block=True)

@test.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    await test.finish("!")
