from nonebot import on_command
from nonebot.adapters import Bot


ping = on_command("ping", priority=1, block=True)

@ping.handle()
async def handle(bot: Bot):
    await ping.finish("ムラサメです！")
