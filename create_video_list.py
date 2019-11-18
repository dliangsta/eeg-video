import glob
with open("/share/pi/cleemess/file-conversion-pipeline/all_mp4s.txt", "w") as f:
  for fn in glob.glob("/share/pi/cleemess/file-conversion-pipeline/*/*/*/*/*.mp4"):
    f.write(fn + "\n")