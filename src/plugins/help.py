from nonebot import on_command
from nonebot.adapters import Bot


help = on_command("help", priority=1, block=True)

@help.handle()
async def handle(bot: Bot):
    await help.finish("""小从雨现在可以
/help : 呃啊
/ping : 歪？是小从雨吗？
/roll <number=100> : 在 [0, number] 里摇点
/roll [arg1] [arg2] <...> : 专治选择困难""")
