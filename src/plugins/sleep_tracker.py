from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP

from pathlib import Path
from pickle import dump, load
from datetime import datetime


# data 存储结构：
# {
#   gid<int>: {
#     date<date>: {
#       uid<int>: [sleeptime<datetime.datetime>, wakeuptime<datetime.datetime>]
#     }
#   }
# }


# 得到当前文件绝对路径 + data 路径
data_path = str(Path(__file__).parent.absolute()) + "/../data/sleep_tracker_data.pickle"

# 若数据文件不存在则先创建空数据文件
try:
    f = open(data_path, "rb")
    f.close()
except FileNotFoundError:
    data = {}
    f = open(data_path, "wb")
    dump(data, f)
    f.close()


good_night = on_command("晚安", permission=GROUP, priority=3, block=True)

@good_night.handle()
async def handle_en(bot: Bot, event: MessageEvent):
    f = open(data_path, "rb")
    data = load(f)
    f.close()

    session_id = event.get_session_id().split("_")
    gid = int(session_id[1])
    uid = int(event.get_user_id())
    time = datetime.now()
    date = time.date()

    if gid in data:
        if date in data[gid]:
            # if uid in data[gid][date]:
            #     data[gid][date][uid] = [time, -1]
            # else:
            #     data[gid][date][uid] = [time, -1]
            data[gid][date][uid] = [time, -1]
        else:
            data[gid][date] = {
                uid: [time, -1]
            }
    else:
        data[gid] = {
            date: {
                uid: [time, -1]
            }
        }

    f = open(data_path, "wb")
    dump(data, f)
    f.close()

    await good_night.finish("晚安哦" + MessageSegment.at(uid) + f"\n[debug msg]:\n{data[gid][date][uid]}")
