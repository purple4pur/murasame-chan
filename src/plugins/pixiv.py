from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment, unescape

import re
import httpx
import feedparser
import httpcore
from random import choice


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
        is_timeout, is_error, status, data = await get_image_data_v1(url="https://rakuen.thec.me/PixivRss/daily-10")
    elif argc > 0 and state["arg1"] == "周榜":
        is_timeout, is_error, status, data = await get_image_data_v1(url="http://rakuen.thec.me/PixivRss/weekly-10")
    elif argc > 0 and state["arg1"] == "月榜":
        is_timeout, is_error, status, data = await get_image_data_v1(url="https://rakuen.thec.me/PixivRss/monthly-10")
    elif argc > 0:
        keyword = unescape(state["arg1"])
        await pixiv.send(f"正在搜索[{keyword}]……")
        is_timeout, is_error, status, data = await get_image_data_v2(tag=keyword)
    else:
        is_timeout, is_error, status, data = await get_image_data_v2()

    uid = event.user_id
    session_id = event.get_session_id().split("_")
    # 消息来自群聊
    if len(session_id) == 3:
        at = MessageSegment.at(uid) + "\n"
    else:
        at = ""

    if is_timeout:
        await pixiv.finish(at + "苦しい……请求超时了(´。＿。｀)")
    if status != 200 and status != 0:
        await pixiv.finish(at + f"苦しい……连接出错了({status})，可以马上重试一下呢！")
    if is_error:
        await pixiv.finish(at + "苦しい……连接出错了(´。＿。｀)")
    elif len(data) == 0:
        await pixiv.finish(at + "寂しい……什么都没找到呢。试试范围更大的关键词哦！")
    else:
        chosen = choice(data)
        await pixiv.send(at + f"{chosen[0]}\nPixiv 链接：{chosen[1]}\n" + MessageSegment.image(chosen[2]) + "似乎发不出图片了呜呜，复制图片链接到浏览器查看吧")
        await pixiv.finish(at + chosen[2])


async def get_image_data_v2(tag: str = None, timeout: int = 30) -> (bool, bool, int, list):
    '''
    获取图片信息函数 v2 版，采用 Lolicon API (https://api.lolicon.app/#/setu)

    `returns` : 是否超时，是否连接出错，状态码，data 数组
    '''
    url_base = "https://api.lolicon.app/setu/v2"
    data = []

    async with httpx.AsyncClient(timeout=timeout) as client:
        # 未指定关键词，返回随机图片
        if tag is None:
            r = await client.get(url_base)

        # 按关键词搜索
        else:
            params = {"tag": tag}
            r = await client.get(url_base, params=params)

        # 处理返回数据
        if r.status_code == 200 and len(r.json()["data"]) != 0:
            d = r.json()["data"][0]  # dict，图片信息
            data.append([
                d["title"],                      # 标题
                "pixiv.net/i/" + str(d["pid"]),  # pixiv 地址
                d["urls"]["original"]            # 图片镜像链接
            ])

    return (False, False, r.status_code, data)


async def get_image_data_v1(url: str = None, keyword: str = None, timeout: int = 30) -> (bool, bool, int, list):
    '''
    获取图片信息函数 v1 版，按关键词搜索采用 rsshub.app API (https://docs.rsshub.app/social-media.html#pixiv)

    `returns` : 是否超时，是否连接出错，状态码，data 数组
    '''
    data = []

    if keyword:
        url = f"https://rsshub.app/pixiv/search/{keyword}/popular/1"

    try:
        rss, status = await async_feedparser(url, timeout)

    # 连接超时
    except (httpx.TimeoutException, httpcore.TimeoutException):
        return (True, False, 0, data)
    # 连接出错
    except (httpx.NetworkError, httpcore.NetworkError):
        return (False, True, 0, data)

    else:
        for entry in rss["entries"]:
            data.append([entry["title"], entry["link"], entry["summary"]])
        for item in data:
            item[1] = item[1][12:].replace("artworks", "i")
            item[2] = re.findall(r"src=.+?jpg", item[2])[0][5:]
        return (False, False, status, data)


async def async_feedparser(url="", timeout=30):
    data = {'entries': []}
    status_code = 0

    async with httpx.AsyncClient(timeout=timeout) as client:
        feed = await client.get(url)
        status_code = feed.status_code
        if status_code == 200:
            data = feedparser.parse(feed.text)

    return (data, status_code)
