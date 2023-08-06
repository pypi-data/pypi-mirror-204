"""Test out the split window videos"""

import fmdt
import os

dir = "/home/ejovo/Videos/Window/window_3_sony_0400-0405UTC"

files = os.listdir(dir)

print(files)

for f in files:
    full_path = dir + "/" + f
    
    (fmdt
        .detect(
            vid_in_path=full_path,
            trk_out_path="trk.txt",
            trk_bb_path="bb.txt",
            light_min=75,
            light_max=100)
        .visu())

# Let's play around with the second file

v = files[1]

