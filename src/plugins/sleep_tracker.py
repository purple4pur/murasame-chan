from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP

from pathlib import Path
from pickle import dump, load


# data 存储结构：
# {
#   gid: {
#     day: {
#       uid: [sleeptime, wakeuptime]
#     }
#   }
# }


# 得到当前文件绝对路径 + data 路径
data_path = str(Path(__file__).parent.absolute()) + "/../data/sleep_tracker_data.pickle"

try:
    f = open(data_path, "rb")
    f.close()
except FileNotFoundError:
    data = {}
    f = open(data_path, "wb")
    dump(data, f)
    f.close()


# good_night = on_command("晚安", permission=GROUP, priority=3, block=True)

# @good_night.handle()
# async def handle_en(bot: Bot):
#     await good_night.finish()
