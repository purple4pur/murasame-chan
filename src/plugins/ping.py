from nonebot import on_command, matcher
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


ping = on_command("ping", priority=5)

@ping.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    await ping.finish("ムラサメです！")
