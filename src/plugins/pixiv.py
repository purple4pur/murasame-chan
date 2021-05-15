from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment

import feedparser
import re
import socket
from random import choice
from urllib.parse import quote
from urllib.error import URLError
from feedparser_data import RssAsync


# 设置全局 timeout
# socket.setdefaulttimeout(10)


pixiv = on_command("给点", priority=1, block=True)

@pixiv.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    raw_args = str(event.get_message()).strip()
    argc = 0
    if raw_args:
        arg_list = raw_args.split()
        argc = len(arg_list)
        for i in range(argc):
            state[f"arg{i+1}"] = arg_list[i]

    if argc > 0 and state["arg1"] == "日榜":
        is_timeout, status, data = await get_image_data(url="https://rakuen.thec.me/PixivRss/daily-20")
    elif argc > 0:
        keyword = state["arg1"]
        await pixiv.send(f"正在找[{keyword}]……")
        is_timeout, status, data = await get_image_data(keyword=keyword)
    else:
        is_timeout, status, data = await get_image_data(url="https://rakuen.thec.me/PixivRss/weekly-30")

    if is_timeout:
        await pixiv.finish("苦しい……请求超时了，稍后重试一下呢")
    elif status != 200:
        await pixiv.finish(f"苦しい……访问出错了({status})，稍后重试一下呢")
    elif len(data) == 0:
        await pixiv.finish("寂しい……什么都没有呢")
    else:
        chosen = choice(data)
        await pixiv.finish(f"{chosen[0]}\n{chosen[1]}\n" + MessageSegment.image(chosen[2]))


async def get_image_data(url: str = None, keyword: str = None) -> (bool, int, list):
                                                            # 是否超时，状态码，data 数组
    data = []

    if keyword:
        url = f"https://rsshub.app/pixiv/search/{quote(keyword)}/popular/1"

    try:
        rss = await RssAsync.get_data(url_to_parse=url, bypass_bozo=True)

    # 请求超时
    except (socket.timeout, URLError):
        return (True, None, data)

    else:
        for entry in rss["entries"]:
            data.append([entry["title"], entry["link"], entry["summary"]])
        for item in data:
            item[1] = item[1][12:].replace("artworks", "i")
            item[2] = re.findall(r"src=.+?jpg", item[2])[0][5:]
        return (False, rss["status"], data)
