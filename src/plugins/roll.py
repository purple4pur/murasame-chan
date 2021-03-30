from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from random import randint


roll = on_command("roll", rule=to_me(), priority=5)

@roll.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
        state["arg1"] = arg_list[0]
        # for i in range(len(arg_list)):
        #     state[f"arg{i+1}"] = arg_list[i]

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
        await roll.finish(f"[roll in 0~{max}]:\n{r}")
    else:
        await roll.finish("Invalid input!")
