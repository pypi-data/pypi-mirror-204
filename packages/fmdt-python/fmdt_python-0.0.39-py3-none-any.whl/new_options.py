import fmdt

window = fmdt.load_window()
clips = window[0].create_clips()
c = clips[-1]

trk_rates = []

for lmin in range(50, 150, 5):

    # Call detect with varying (lmin, lmax)
    res = c.detect(
            light_min = lmin, 
            light_max = lmin + 5
          )

    # Retreive the trk_rate 
    trk_rate = res.check().trk_rate()

    print(f"({lmin}, {lmin + 5}) -> {trk_rate}")



