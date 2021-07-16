from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, escape


say = on_command("say", permission=SUPERUSER, priority=1, block=True)

@say.handle()
async def handle(bot: Bot, event: MessageEvent):
    msg = str(event.get_message()).strip()
    await say.finish(escape(msg))
