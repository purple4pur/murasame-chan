from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment
from nonebot.permission import SUPERUSER

import feedparser
import re
from random import choice
from urllib.parse import quote


pixiv_search = on_command("test给点", permission=SUPERUSER, priority=1, block=True)

@pixiv_search.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
        argc = len(arg_list)
        for i in range(argc):
            state[f"arg{i+1}"] = arg_list[i]

    await pixiv_search.send("正在搜索[" + state["arg1"] + "]，请耐心等待...")

    data = await get_image_data(keyword=state["arg1"])
    chosen = choice(data)
    await pixiv_search.finish(f"{chosen[0]}\n{chosen[1]}\n" + MessageSegment.image(chosen[2]))


pixiv_daily = on_command("给点", priority=1, block=True)

@pixiv_daily.handle()
async def handle(bot: Bot, event: MessageEvent):
    data = await get_image_data(url="https://rakuen.thec.me/PixivRss/daily-30")
    chosen = choice(data)
    await pixiv_daily.finish(f"{chosen[0]}\n{chosen[1]}\n" + MessageSegment.image(chosen[2]))


async def get_image_data(url: str = None, keyword: str = None) -> list:
    data = []

    if keyword:
        url = f"https://rsshub.app/pixiv/search/{quote(keyword)}/popular/1"

    rss = feedparser.parse(url)
    for entry in rss["entries"]:
        data.append([entry["title"], entry["link"], entry["summary"]])

    for item in data:
        item[1] = item[1][12:]
        item[2] = re.findall(r"src=.+?jpg", item[2])[0][5:]

    return data
