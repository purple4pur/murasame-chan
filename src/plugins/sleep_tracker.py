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

# 若数据文件不存在则先创建
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

    if gid != 595741581: ######################## FOR DEBUG
        return

    # 5:00 ~ 21:00 拒绝命令
    if 5 <= time.hour < 21:
        await good_night.finish("太早啦，还没到说晚安的时候呢！不要跟小丛雨开玩笑了啦……")
        return

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

    debug_msg = f"""\n\n[debug msg]:
gid = {gid}
uid = {uid}
time = {time}
date = {date}
datetime_list={data[gid][date][uid]}"""

    await good_night.finish("晚安啦" + MessageSegment.at(uid) + "，要说到做到哦！" + debug_msg)


good_morning = on_command("早", permission=GROUP, priority=3, block=True)

@good_morning.handle()
async def handle_en(bot: Bot, event: MessageEvent):
    session_id = event.get_session_id().split("_")
    gid = int(session_id[1])
    uid = int(event.get_user_id())
    time = datetime.now()
    date = time.date()

    if gid != 595741581: ######################## FOR DEBUG
        return

    # 14:00 ~ 次日 3:00 拒绝命令
    if time.hour < 3 or time.hour >= 14:
        await good_morning.finish("早上好……诶！怎么想都不太对吧！")
        return

    # 起床时间储存到前一天的数据里
    date -= timedelta(1)

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
    try:
        if time_list[0] != -1:
            delta = time_list[1] - time_list[0]
            hours, remains = divmod(delta.seconds, 3600)
            mins, secs = divmod(remains, 60)

            sleep_time_info = f"昨晚你睡了{hours}小时{mins}分哦！"
        else:
            delta = -1
            sleep_time_info = "没有记录到你的睡觉时间呢，下次记得跟小丛雨说晚安哦！"

        debug_msg = f"""\n\n[debug msg]:
gid = {gid}
uid = {uid}
time = {time}
date = {date}
datetime_list={data[gid][date][uid]}"""

        await good_morning.finish("你醒啦！" + MessageSegment.at(uid) + sleep_time_info + debug_msg)
    except:
        await good_morning.finish("小丛雨出错啦，苦しい……可以重试一下呢！")
