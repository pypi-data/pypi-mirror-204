import fmdt
import os


def _mkdirp(dir: str):
    if not os.path.exists(dir):
        os.mkdir(dir)

# ============== Videos ==================================
d6 = fmdt.load_draco6(require_gt=True)
d12 = fmdt.load_draco12(require_gt=True)

# ============= GroundTruth (list[HumanDetection]) ======
gt6 = fmdt.load_gt6()
gt12 = fmdt.load_gt12()

print(d6)
print(d12)

print(gt6)
print(gt12)

args = fmdt.Args.new(light_min=253, light_max=255, timeout=0.5, log_path="log", log=True)

results = []

print(len(d6))

for i in range(len(d6)):
    v = d6[i]
    
    args.detect_args.vid_in_path = v.full_path()
    # args.detect_args.trk_out_path = v.default_trk_path()
    args.detect_args.trk_out_path = args.detect_args.cache_trk()
    args.detect_args.log_path = args.detect_args.cache_dir()

    _mkdirp(args.detect_args.cache_dir())
    results.append(args.detect())

for r in results:
    print(r.to_dataframe())

# list_bools = [v.check_args(args) for v in d6]

# for i in range(len(list_bools)):

#     def one_or_more_det(bools: list[bool]):
#         for b in bools:
#             if b:
#                 return b
    

# Keep the videos that had a detection with args

# vids_with_det = [d6[i] for i in range(len(list_bools)) if one_or_more_det(list_bools[i])]

# print(vids_with_det)
# print(f"# of vids with detected meteors: {len(vids_with_det)}")

# # I want to visualize each video that was detected

# for v in vids_with_det:
#     fmdt.visu(vid_in_path=v.full_path(), vid_out_path=v.visu_name(), )