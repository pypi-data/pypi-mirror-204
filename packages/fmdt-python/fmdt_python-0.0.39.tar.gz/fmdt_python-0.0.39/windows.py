import fmdt
import pandas as pd
import numpy as np


# Let's evaluate how well light min and light max play with our windows videos
def score_window(clips: list[fmdt.VideoClip], light_min = 55, light_max = 80) -> pd.DataFrame:
    """Return a list containing the trk rates for each individual clip"""
    rates = []

    for c in clips:
        d_res = c.detect(light_min=light_min, light_max=light_max)
        if len(d_res.trk_list) > 0:
            c_res = d_res.check()
            rates.append(c_res.trk_rate())
        else:
            rates.append(0.0)

    n = len(clips)

    clips_id = range(0, n)
    lmins = np.full(n, light_min)
    lmaxs = np.full(n, light_max)

    return pd.DataFrame({
        "clip_id": clips_id,
        "lmin": lmins,
        "lmax": lmaxs,
        "trk_rate": rates
    })

def score_window_lmin_lmax(window: fmdt.Video, lmin_min, lmin_max, diff):

    clips = window.create_clips()

    # Make sure the clips exist on disk
    for c in clips:
        if not c.exists():
            c.save()

    df = score_window(clips)

    for lmin in range(lmin_min, lmin_max + diff, diff):
        df = pd.concat([df, score_window(clips, lmin, lmin + diff)])
    
    df.to_csv(f"{window.prefix()}_{lmin_min}_{lmin_max}_{diff}_data.csv", index=False)

    
windows = fmdt.load_window()
windows = windows[2:-2]

# Now let's get some light_min and light_max variation
lmin_min = 50
lmin_max = 200 

# score_window_lmin_lmax(windows[0], lmin_min, lmin_max, 1)
# score_window_lmin_lmax(windows[0], lmin_min, lmin_max, 2)
# score_window_lmin_lmax(windows[0], lmin_min, lmin_max, 4)
# score_window_lmin_lmax(windows[0], lmin_min, lmin_max, 8)

# score_window_lmin_lmax(windows[1], lmin_min, lmin_max, 1)
# score_window_lmin_lmax(windows[1], lmin_min, lmin_max, 2)
# score_window_lmin_lmax(windows[1], lmin_min, lmin_max, 4)
# score_window_lmin_lmax(windows[1], lmin_min, lmin_max, 8)

diffs = [1, 2, 4, 8]

for w in windows:
    for d in diffs:
        score_window_lmin_lmax(w, lmin_min, lmin_max, d)
