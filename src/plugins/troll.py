from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent

from random import randint, choice


roll = on_command("troll", priority=5)

@roll.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    argc = 0
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
        argc = len(arg_list)
        for i in range(argc):
            state[f"arg{i+1}"] = arg_list[i]


    # 摇点
    if argc <= 1:
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
            await roll.finish(f"{event.sender.nickname}({event.get_user_id()}) 摇了 {r}！" + ending)
        else:
            await roll.finish("小从雨只会摇正整数哦！")


    # 摇选项
    else:
        start = ["当然是", "必然", "这不得"]
        end = ["啦！", "。", "？"]
        r = randint(0, len(start)-1)
        await roll.finish(f"{start[r]}{choice(arg_list)}{end[r]}")
