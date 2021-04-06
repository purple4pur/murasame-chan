from nonebot import on_command
from nonebot.adapters import Bot


help = on_command("help", priority=1, block=True)

@help.handle()
async def handle(bot: Bot):
    await help.finish("""小从雨现在可以
/help : 呃啊
/ping : 歪？是小从雨吗？
/roll <number=100> : 在 [0, number] 里摇点
/roll [arg1] [arg2] <...> : 专治选择困难
/[...是不是/要不要...] : 快跑！人工智障！
/[sleep/睡觉] : 睡觉啦睡觉啦zzz""")
