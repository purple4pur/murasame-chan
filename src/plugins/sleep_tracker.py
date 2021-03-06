# 在异步 io 的系统里用读写文件来管理数据状态...
# ...这种事情怎么想都很奇怪吧！  Σ(ﾟдﾟ;)
# 但是太懒了不想写数据库呜呜呜
# 低情商：写数据库好麻烦
# 高情商：便于移殖  ( •̀ ω •́ )✧

# 迟到的 edit :
# 好耶用内存！全到存到内存里！


from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP

import atexit
from pathlib import Path
from pickle import dump, load
from datetime import datetime, timedelta


# data 存储结构：
# {
#   gid<int>: {
#     date<datetime.date>: {
#       uid<int>: [入睡时间<datetime.datetime>, 起床时间<datetime.datetime>],
#       -1: [已睡人数<int>, 已起人数<int>]
#     }
#   }
# }


# 得到当前文件绝对路径 + data 路径
data_path = str(Path(__file__).parent.absolute()) + "/../data/sleep_tracker_data.pickle"

# 若数据文件不存在则先创建
try:
    f = open(data_path, "rb")
    f.close()
except FileNotFoundError:
    data = {}
    f = open(data_path, "wb")
    dump(data, f)
    f.close()
    print("[sleep_tracker.py]: 未找到 data 数据文件，已创建空数据文件。")
else:
    print("[sleep_tracker.py]: 找到现有 data 数据文件，将继续使用此数据文件。")
finally:
    f = open(data_path, "rb")
    data = load(f)
    f.close()
    print("[sleep_tracker.py]: 已读取数据文件。")


def save_to_file(data: dict):
    f = open(data_path, "wb")
    dump(data, f)
    f.close()

def save_at_exit(data: dict):
    save_to_file(data)
    print("[sleep_tracker.py]: 已将 data 保存至数据文件。")

atexit.register(save_at_exit, data)


good_night = on_command("晚安", permission=GROUP, priority=3, block=True)

@good_night.handle()
async def handle_night(bot: Bot, event: MessageEvent):
    session_id = event.get_session_id().split("_")
    gid = int(session_id[1])
    uid = int(event.get_user_id())
    time = datetime.now()
    date = time.date()

    # 5:00 ~ 21:00 拒绝命令
    if 5 <= time.hour < 21:
        await good_night.finish("太早啦，还没到说晚安的时候呢！不要跟小丛雨开玩笑了啦……")
        return

    # 5:00 前收到的晚安命令算到前一天里
    if time.hour < 5:
        date -= timedelta(days=1)

    # 存入入睡时间
    if gid in data:
        if date in data[gid]:
            if uid in data[gid][date]:

                # 如果已有入睡时间，刷新为新时间
                if data[gid][date][uid][0] != -1:
                    data[gid][date][uid][0] = time
                    await good_night.finish("哼！不是已经说好了要睡觉了嘛！这次就原谅你了，赶快睡觉吧zzz")
                    return

                data[gid][date][uid][0] = time
            else:
                data[gid][date][uid] = [time, -1]
            data[gid][date][-1][0] += 1
        else:
            data[gid][date] = {
                -1: [1, 0],
                uid: [time, -1]
            }
    else:
        data[gid] = {
            date: {
                -1: [1, 0],
                uid: [time, -1]
            }
        }
    save_to_file(data)

    order = data[gid][date][-1][0]
    await good_night.finish(MessageSegment.at(uid) + f"晚安啦，你是本群第 {order} 个睡觉的人！记得睡觉要说到做到哦！")


good_morning = on_command("早", permission=GROUP, priority=3, block=True)

@good_morning.handle()
async def handle_morning(bot: Bot, event: MessageEvent):
    session_id = event.get_session_id().split("_")
    gid = int(session_id[1])
    uid = int(event.get_user_id())
    time = datetime.now()
    date = time.date()

    # 起床时间储存到前一天的数据里
    date -= timedelta(days=1)

    # 0:00 ~ 3:00 及 14:00 ~ 24:00 拒绝命令
    if time.hour < 3 or time.hour >= 14:
        await good_morning.finish("早上好……诶！怎么想都不太对吧！")
        return

    # 存入起床时间
    if gid in data:
        if date in data[gid]:
            if uid in data[gid][date]:

                # 如果已有起床时间，不作理会
                if data[gid][date][uid][1] != -1:
                    await good_morning.finish("你已经跟小丛雨说过早上好啦！难道睡回笼觉了吗，要是这样小丛雨可要批评你了！")
                    return

                data[gid][date][uid][1] = time
            else:
                data[gid][date][uid] = [-1, time]
            data[gid][date][-1][1] += 1
        else:
            data[gid][date] = {
                -1: [0, 1],
                uid: [-1, time]
            }
    else:
        data[gid] = {
            date: {
                -1: [0, 1],
                uid: [-1, time]
            }
        }
    save_to_file(data)

    time_list = data[gid][date][uid]
    order = data[gid][date][-1][1]
    if time_list[0] != -1:
        delta = time_list[1] - time_list[0]
        hours, remains = divmod(delta.seconds, 3600)
        mins, secs = divmod(remains, 60)

        sleep_time_info = f"昨晚你睡了 {hours} 小时 {mins} 分，是本群起床第 {order} 人！"
    else:
        sleep_time_info = f"你是本群起床第 {order} 人！没有记录到你昨晚的入睡时间呢，今晚记得跟小丛雨说晚安哦！"

    await good_morning.finish(MessageSegment.at(uid) + "你醒啦！" + sleep_time_info)
