from nonebot import on_command


help = on_command("help", priority=5)

@help.handle()
async def handle():
    await help.finish("""小从雨现在可以
/help          : 显示此帮助菜单
/ping          : 看看一下小从雨在不在
/roll <number> : 在 [0, number] 内摇点
""")
