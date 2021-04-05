from nonebot import on_command
from nonebot.rule import keyword
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from random import randint


artificial_idiot = on_command("", rule=keyword("不"), priority=2, block=True)

@artificial_idiot.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message())
    l = len(msg)

    # 循环找到每一个「不」
    index = -1
    while index < l:
        index = msg.find("不", index+1)
        if index == -1:
            break

        # 「不」不位于首尾
        if 0 < index < l-1:
            left = msg[index-1]
            right = msg[index+1]

            # 「不」左右相同
            if left == right:
                # 「你」「我」互换
                msg = msg.replace("你", "&*temp$#")
                msg = msg.replace("我", "你")
                msg = msg.replace("&*temp$#", "我")
                # 「？」换为「！」
                msg = msg.replace("？", "！")
                # 「?」换为「!」
                msg = msg.replace("?", "!")

                # 随机选取结果
                r = randint(0, 1)
                if r == 1:
                    # 截取 [A是]不是[B]
                    await artificial_idiot.finish(msg[:index] + msg[index+2:])
                else:
                    # 截取 [A]是[不是B]
                    await artificial_idiot.finish(msg[:index-1] + msg[index:])
                break
