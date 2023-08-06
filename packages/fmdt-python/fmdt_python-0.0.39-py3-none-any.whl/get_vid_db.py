import os
import fmdt
import fmdt.args
import sqlite3

w6 = "/run/media/ejovo/Seagate Portable Drive/Meteors/Watec6mm/Meteor"
w12 = "/run/media/ejovo/Seagate Portable Drive/Meteors/Watec12mm/Meteor"
win = "/run/media/ejovo/Seagate Portable Drive/Meteors"


def is_video(vid_name: str) -> bool:
    return vid_name[-3:] == "avi" or vid_name[-3:] == "mp4"

def is_draco6(vid_name: str) -> bool:
    return is_video(vid_name) and vid_name[0:13] == "Draconids-6mm"

def is_draco12(vid_name: str) -> bool:
    return is_video(vid_name) and vid_name[0:14] == "Draconids-12mm"

def is_window(vid_name: str) -> bool:
    return is_video(vid_name) and vid_name[0:6] == "window"


# def get_vids(dir: str, type: fmdt.args.VideoType) -> list[]

def get_draco6(dir) -> list[fmdt.args.Video]:
    return [fmdt.Video(v, type=fmdt.args.VideoType.DRACO6) for v in os.listdir(dir) if is_draco6(v)]

def get_draco12(dir) -> list[fmdt.args.Video]:
    return [fmdt.Video(v, type=fmdt.args.VideoType.DRACO12) for v in os.listdir(dir) if is_draco12(v)]

def get_window(dir) -> list[fmdt.args.Video]:
    return [fmdt.Video(v, type=fmdt.args.VideoType.WINDOW) for v in os.listdir(dir) if is_window(v)]

d6 = get_draco6(w6)
d12 = get_draco12(w12)
dw = get_window(win)

d6.sort()
d12.sort()
dw.sort()

print(d6)
print()
print(d12)

print(len(d6))
print(len(d12))
print(len(dw))

all = [v for v in d6]
all.extend(d12)
all.extend(dw)

print(len(all))
print(type(all[0]))

fmdt.args.videos_to_csv(all, "test_vid.csv")
# videos = fmdt.args.csv_to_videos("test_vid.csv")
# print(len(videos))

# for i in range(10):


