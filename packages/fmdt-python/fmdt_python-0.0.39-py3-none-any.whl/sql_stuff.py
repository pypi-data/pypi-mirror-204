"""Convert the contents of `human_detectsions.csv` and `test_vid.csv` and "meteors.txt" into a single data base file `videos.db`"""

import sqlite3 
import pandas as pd
from fmdt.args import *
import fmdt.truth

f = open("videos.db", "w")
f.close()

con = sqlite3.connect("videos.db")

cur = con.cursor()

cur.execute("CREATE TABLE video(id, name, type)")

# Let's load in our csv
df = pd.read_csv("test_vid.csv")
print(df.head(10))

for i in range(len(df)):
    r = df.iloc[i]

    id = r["id"]
    name = r["name"]
    type = r["type"]


    # print(id)
    # print(name)
    # print(type)
    cur.execute(f"""
    INSERT INTO video VALUES 
        ({id}, '{name}', '{type}')
    """)

#================ GroundTruths ===================
# fmdt.truth.GroundTruth("")
# fmdt.truth.init_ground_truth()
csv_file = "human_detections.csv"

df_gt = pd.read_csv(csv_file)

# Pandas DataFrame Ground Truths
cur.execute("CREATE TABLE human_detection(id, video_name, start_x, start_y, start_frame, end_x, end_y, end_frame)")
for i in range(len(df_gt)):
    r = df_gt.iloc[i]

    vid_name = r["video_name"]
    start_x = r["start_x"]
    start_y = r["start_y"]
    start_frame = r["start_frame"]
    end_x = r["end_x"]
    end_y = r["end_y"]
    end_frame = r["end_frame"]

    cur.execute(f"""
    INSERT INTO human_detection VALUES 
        ({i}, '{vid_name}', {start_x}, {start_y}, {start_frame}, {end_x}, {end_y}, {end_frame})
    """)

print(i)

import fmdt.db
import fmdt.truth

# ================= Ground Truths in meteors.txt ========
meteors = fmdt.truth.load_meteors_file("meteors.txt", "2022_05_31_tauh_34_meteors.mp4")

start = i + 1
for i in range(start, start + len(meteors)):
    m = meteors[i - start]

    query = f"""
    INSERT INTO human_detection VALUES 
        ({i}, '{m.video_name}', {m.start_x}, {m.start_y}, {m.start_frame}, {m.end_x}, {m.end_y}, {m.end_frame})
    """

    cur.execute(query)

con.commit()
con.close()

