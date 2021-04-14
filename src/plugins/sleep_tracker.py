# 在异步 io 的系统里用读写文件来管理数据状态...
# ...这种事情怎么想都很奇怪吧！  Σ(ﾟдﾟ;)
# 但是太懒了不想写数据库呜呜呜
# 低情商：写数据库好麻烦
# 高情商：便于移殖  ( •̀ ω •́ )✧


from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP

from pathlib import Path
from pickle import dump, load
from datetime import datetime, timedelta


# data 存储结构：
# {
#   gid<int>: {
#     date<datetime.date>: {
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
    session_id = event.get_session_id().split("_")
    gid = int(session_id[1])
    uid = int(event.get_user_id())
    time = datetime.now()
    date = time.date()

    f = open(data_path, "rb")
    data = load(f)
    f.close()

    if gid in data:
        if date in data[gid]:
            if uid in data[gid][date]:
                data[gid][date][uid][0] = time
            else:
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


good_morning = on_command("早", permission=GROUP, priority=3, block=True)

@good_morning.handle()
async def handle_en(bot: Bot, event: MessageEvent):
    session_id = event.get_session_id().split("_")
    gid = int(session_id[1])
    uid = int(event.get_user_id())
    time = datetime.now()
    date = time.date()

    f = open(data_path, "rb")
    data = load(f)
    f.close()

    if gid in data:
        if date in data[gid]:
            if uid in data[gid][date]:
                data[gid][date][uid][1] = time
            else:
                data[gid][date][uid] = [-1, time]
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

    time_list = data[gid][date][uid]
    if time_list[0] != -1:
        delta = time_list[1] - time_list[0]
        hours, remains = divmod(delta.seconds, 3600)
        mins, secs = divmod(remains, 60)

        ending = f"昨晚你睡了{hours}小时{mins}分哦！"
    else:
        delta = -1  #########################################
        ending = "没有记录到你的睡觉时间呢"

    await good_morning.finish("你醒辣！" + MessageSegment.at(uid) + ending + f"\n[debug msg]:\ntime_list={data[gid][date][uid]}\ndelta={delta}")
