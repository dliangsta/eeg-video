import subprocess
import os

from multiprocessing import Pool
from random import shuffle
from tqdm import tqdm
from glob import glob


def convert_wmv_to_mp4(arg):
  wmv_fn, mp4_fn = arg
  if not os.path.exists(mp4_fn):
    try:
      subprocess.call([
        "ffmpeg", 
        "-r", 
        "30000/1001", 
        "-i", 
        wmv_fn, 
        "-r", 
        "30000/1001", 
        "-movflags", 
        "+faststart", 
        "-c:v", 
        "libx264", 
        "-crf", 
        "23", 
        "-c:a", 
        "aac", 
        "-q:a", 
        "100",
        mp4_fn
      ], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    except Exception as e:
      print("error!\n\n")
      print(e)
          

if __name__ == "__main__":


  # with open("/share/pi/cleemess/file-conversion-pipeline/bad_mp4s.txt", "r") as f:
  #   fns = [line.strip() for line in f.readlines()]
  #   for fn in fns:
  #     if os.path.exists(fn):
  #       os.remove(fn)
  #     assert not os.path.exists(fn)

  wmv_fns = glob("/share/pi/cleemess/file-conversion-pipeline/*/*/*/*/*.WMV")
  mp4_fns = glob("/share/pi/cleemess/file-conversion-pipeline/*/*/*/*/*.mp4")

  fns = []
  for wmv_fn in wmv_fns:
    mp4_fn = wmv_fn.replace(".WMV", ".mp4")
    if not os.path.exists(mp4_fn):
      fns.append((wmv_fn, mp4_fn))

  # assert len(set(wmv_fns)) - len(set(mp4_fns)) == len(fns), (len(set(wmv_fns)), len(set(mp4_fns)), len(set(wmv_fns)) - len(set(mp4_fns)), len(fns), list(set(wmv_fns) - set(mp4_fns)), fns)

  shuffle(fns)
  p = Pool(16)
  # p.map(convert_wmv_to_mp4, fns)
  for _ in tqdm(p.imap_unordered(convert_wmv_to_mp4, fns), total=len(fns)):
    pass

  # with tqdm(fns) as pbar:
  #   for wmv_fn, mp4_fn in pbar:
  #     if not os.path.exists(mp4_fn):
  #       pbar.set_description(mp4_fn)
  #       convert_wmv_to_mp4(wmv_fn, mp4_fn)
