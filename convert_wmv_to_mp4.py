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
      subprocess.call(["ffmpeg", "-i", wmv_fn, mp4_fn], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    except Exception as e:
      print("error!\n\n")
      print(e)
          

if __name__ == "__main__":
  wmv_fns = glob("/share/pi/cleemess/file-conversion-pipeline/*/*/*/*/*.WMV")
  mp4_fns = glob("/share/pi/cleemess/file-conversion-pipeline/*/*/*/*/*.mp4")

  fns = []
  for wmv_fn in wmv_fns:
    mp4_fn = wmv_fn.replace(".WMV", ".mp4")
    if not os.path.exists(mp4_fn):
      fns.append((wmv_fn, mp4_fn))

  assert len(set(wmv_fns)) - len(set(mp4_fns)) == len(fns)

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
