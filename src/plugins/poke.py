from nonebot import on_notice
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.adapters.cqhttp.event import PokeNotifyEvent
from nonebot.adapters.cqhttp.exception import ActionFailed

from pathlib import Path
from random import choice


BOT_ID = 2497540344

images_urls = [
    # "selection-mod-doubletime@2x.png",
    "selection-mod-fadein@2x.png",
    "selection-mod-flashlight@2x.png",
    "selection-mod-hardrock@2x.png",
    "selection-mod-hidden@2x.png",
    "selection-mod-nightcore@2x.png",
    # "selection-mod-perfect@2x.png",
    # "selection-mod-relax@2x.png",
    # "selection-mod-relax2@2x.png",
    "selection-mod-spunout@2x.png",
    # "selection-mod-suddendeath@2x.png"
]

# 得到当前文件绝对路径
path = Path(__file__).parent.absolute()

def get_avatar_url():
    '''
    随机返回一个图片路径
    '''
    return f"file://{path}/../static/image/{choice(images_urls)}"


poke = on_notice()

@poke.handle()
async def handle_poke(bot: Bot, event: PokeNotifyEvent):
    if event.target_id == BOT_ID:  # 自己被戳
        try:
            await poke.finish(MessageSegment.image(get_avatar_url()))
        except ActionFailed as e:
            print(f"[poke.py]: {e}")
