from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent


print(str.center("文件被运行了！", 40, "="))

repeat = on_message(priority=5, block=False)

@repeat.handle()
async def handle(bot: Bot, event: MessageEvent):
    print(str.center("收到消息", 40, "="))
