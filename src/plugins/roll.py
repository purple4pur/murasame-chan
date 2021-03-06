from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment

from random import randint, choice


roll = on_command("roll", priority=1, block=True)

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
        is_valid = True
        if "arg1" in state:
            try:
                max_num = int(state["arg1"])
            except ValueError:
                max_num = -1
            if max_num <= 0:
                is_valid = False
        else:
            max_num = 100

        if is_valid:
            r = randint(0, max_num)
            ending = "好耶！"
            if r <= round(max_num/3):
                ending = "不会吧不会吧？"
            await roll.finish(MessageSegment.at(event.get_user_id()) + f"摇了 {r}！" + ending)
        else:
            await roll.finish("小丛雨只会摇正整数哦！")


    # 摇选项
    else:
        # 消去重复选项
        arg_list = list(set(arg_list))

        if len(arg_list) > 1:
            start = ["当然是", "必然", "这不得"]
            end = ["啦！", "。", "？"]
            r = randint(0, len(start)-1)
            await roll.finish(f"{start[r]}{choice(arg_list)}{end[r]}")
        else:
            await roll.finish(f"只能是{arg_list[0]}了！你根本就没想让小丛雨帮你决定，哼！")
