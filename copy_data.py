# copies data from /share/pi/cleemess/stanford-eeg-box/stanford to /share/pi/cleemess/file-conversion-pipeline

import shutil
import os

from glob import glob
from tqdm import tqdm


# https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth/31039095
def copytree(src, dst, symlinks=False, ignore=None):
  for item in os.listdir(src):
      s = os.path.join(src, item)
      d = os.path.join(dst, item)
      if os.path.isdir(s):
          shutil.copytree(s, d, symlinks, ignore)
      else:
          shutil.copy2(s, d)


if __name__ == "__main__":
  source_dirs = set(glob("/share/pi/cleemess/stanford-eeg-box/stanford/*/*/*/*/"))


  new_dirs = []
  for source_dir in source_dirs:
    dest_dir = source_dir.replace("stanford-eeg-box/stanford","file-conversion-pipeline")
    dest_parent = "/".join(dest_dir.split("/")[:-2])
    if not os.path.exists(dest_dir):
      new_dirs.append((source_dir, dest_dir))

  for source_dir, dest_dir in tqdm(list(sorted(new_dirs))):
      print(source_dir, dest_dir)
      os.makedirs(dest_dir)
      copytree(source_dir, dest_dir)
