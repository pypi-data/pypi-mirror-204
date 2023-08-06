"""Play with the contents of `videos.db` programmatically and store results in data frames."""

import pandas as pd
import sqlite3
import fmdt.args
import fmdt.truth
import fmdt.config
import fmdt.db


# Add a videos.db file to our config
fmdt.download_csvs()

# config = fmdt.config.load_config()
# files_in_config = fmdt.config.listdir()

# print(files_in_config)
print(f"config directory: {fmdt.config.dir()}")

fmdt.download_dbs()
vids = fmdt.load_draco6() # list[Video]
for i in range(20):
    v = vids[i]
    print(f"{v.id()}: {v} has {len(v.meteors())} meteor(s) in our database")

print(".")
print(".")
print(".")

print(f"{vids[-1].id()}: {vids[-1]} has {len(vids[-1].meteors())} meteor(s) in our database")

id = 17
v = vids[id]
print(f"vids[{id}].meteors() -> {v.meteors()[0]} and has full dir: {v.full_path()}")

on_disc = [v for v in vids if v.exists()]
has_meteors = [v for v in on_disc if v.has_meteors()]

print(f"{len(on_disc)} videos exist on disc out of {len(vids)}")
print(f"{len(has_meteors)} videos have meteors and exist on disk")

# Let's get some diagnostics then.

# Like: How many videos exist from our database exist on disk?

d6 = fmdt.load_draco6()
d12 = fmdt.load_draco12()
w = fmdt.load_window()


fmdt.db.info()

print(w)
print(w[0].full_path())