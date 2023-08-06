import fmdt

vid = "demo.mp4"

# res = fmdt.detect(vid, trk_out_path="trk.txt", log_path="log_path")
res = fmdt.detect(vid, log_path="log")

print(res.nframes)
print(res.to_dataframe())
