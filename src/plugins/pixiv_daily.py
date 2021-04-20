from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment

import feedparser
import re
from random import choice


pixiv_daily = on_command("给点", priority=1, block=True)

@pixiv_daily.handle()
async def handle(bot: Bot, event: MessageEvent):
    data = await get_image_data()
    chosen = choice(data)
    await pixiv_daily.finish(f"{chosen[0]}\n{chosen[1]}\n" + MessageSegment.image(chosen[2]))


async def get_image_data() -> list:
    data = []

    rss = feedparser.parse("https://rakuen.thec.me/PixivRss/daily-20")
    for entry in rss["entries"]:
        data.append([entry["title"], entry["link"], entry["summary"]])

    for item in data:
        item[1] = item[1][12:]
        item[2] = re.findall(r"src=.*jpg", item[2])[0][5:]

    return data
