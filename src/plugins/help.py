from nonebot import on_command
from nonebot.adapters import Bot


help_menu = on_command("help", aliases={"帮助"}, priority=1, block=True)

@help.handle()
async def handle(bot: Bot):
    await help_menu.finish("前往 purple4pur.com/murasame-chan 查看帮助哦！")
