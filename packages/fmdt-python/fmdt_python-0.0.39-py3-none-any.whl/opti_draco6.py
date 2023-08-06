import fmdt

draco12 = fmdt.load_draco6(require_gt = True)
lmin = 232
lmax = 251

res_detect = [d.detect(light_min = lmin, light_max = lmax, timeout = 2) for d in draco12]
res_check  = [r.check() for r in res_detect]
has_detection = [c.trk_rate() > 0.0 for c in res_check]

for r in res_check:
    print(r.all_stats())

print(sum(has_detection))