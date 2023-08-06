import fmdt

args = fmdt.detect_args(vid_in_path="demo.mp4", trk_all=True)

res = args.detect()
print(res.trk_list)
print(len(res.trk_list))