from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment
from nonebot.permission import SUPERUSER

import feedparser
import re
from random import choice


pixiv_daily_r18 = on_command("给点r18", permission=SUPERUSER, priority=1, block=True)

@pixiv_daily_r18.handle()
async def handle(bot: Bot, event: MessageEvent):
    data = await get_image_data("http://rakuen.thec.me/PixivRss/daily_r18-20")
    chosen = choice(data)
    await pixiv_daily_r18.finish(f"{chosen[0]}\n{chosen[1]}\n" + MessageSegment.image(chosen[2]))


pixiv_daily = on_command("给点", priority=2, block=True)

@pixiv_daily.handle()
async def handle(bot: Bot, event: MessageEvent):
    data = await get_image_data("https://rakuen.thec.me/PixivRss/daily-30")
    chosen = choice(data)
    await pixiv_daily.finish(f"{chosen[0]}\n{chosen[1]}\n" + MessageSegment.image(chosen[2]))


async def get_image_data(url: str) -> list:
    data = []

    rss = feedparser.parse(url)
    for entry in rss["entries"]:
        data.append([entry["title"], entry["link"], entry["summary"]])

    for item in data:
        item[1] = item[1][12:]
        item[2] = re.findall(r"src=.*jpg", item[2])[0][5:]

    return data
