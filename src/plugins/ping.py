from nonebot import on_command


ping = on_command("ping", priority=5)

@ping.handle()
async def handle():
    await ping.finish("ムラサメです！")
