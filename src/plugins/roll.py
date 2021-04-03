from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from random import randint


roll = on_command("roll", priority=5)

@roll.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
        state["arg1"] = arg_list[0]

    isValid = True
    if "arg1" in state:
        try:
            max = int(state["arg1"])
        except ValueError:
            max = -1
        if max <= 0:
            isValid = False
    else:
        max = 100

    if isValid:
        r = randint(0, max)
        ending = "好耶！"
        if r <= round(max/3):
            ending = "不会吧不会吧？"
        await roll.finish(f"({event.get_user_id()})摇了 {r}！" + ending)
    else:
        await roll.finish("小从雨现在还只会roll正整数哦！")
