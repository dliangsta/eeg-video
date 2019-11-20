import argparse
import json
import os
import shlex
import subprocess
import sys

from tqdm import tqdm

def generate_video_metadata(absolute_paths):
  
  """
  Scans through files, uses ffprobe to look into the video
  files to obtain video format metadata such as height, width, fps,
  etc.

  Return an array of metadata, one element for each video found in the
  source directory. 

  Although video filenames are unique identifiers, this script also
  assigns each video a unique integer id.

  At this time there is not support for recurive directory tree
  search.  This would be a useful feature to add in the future.

  """

  vids = []

  bad_fn = "/share/pi/cleemess/file-conversion-pipeline/bad_mp4s.txt"
  good_fn = "/share/pi/cleemess/file-conversion-pipeline/good_mp4s.txt"
  # if os.path.exists(bad_fn):
  #   os.remove(bad_fn)

  if os.path.exists(bad_fn):
    with open(bad_fn) as f:
      bad_paths = set([line.strip() for line in f.readlines()])
  else:
    bad_paths = set()

  if os.path.exists(good_fn):
    with open(good_fn) as f:
      good_paths = set([line.strip() for line in f.readlines()])
  else:
    good_paths = set()
  
  with tqdm(list(absolute_paths)) as pbar:
    for absolute_path in pbar:
      if absolute_path in bad_paths or absolute_path in good_paths:
        continue

      cmd = "ffprobe -v quiet -print_format json -show_streams %s" % absolute_path
      try:
        subprocess.check_output(shlex.split(cmd)).decode("utf-8")
        with open(good_fn, "a") as f:
          f.write(absolute_path + "\n")
        good_paths.add(absolute_path)
      except KeyboardInterrupt:
        raise
      except Exception as e:
        with open(bad_fn, "a") as f:
          f.write(absolute_path + "\n")
        bad_paths.add(absolute_path)
        # print(e)
        # print(cmd)
        # raise

      pbar.set_description(f"{len(good_paths)}, {len(bad_paths)}")
  return vids



parser = argparse.ArgumentParser(description='Generate video metadata.')
parser.add_argument('--basedir', help='Base directory containing videos', default="/share/pi/cleemess/file-conversion-pipeline")
parser.add_argument('--file_list', help='List of video files', default="/share/pi/cleemess/file-conversion-pipeline/all_mp4s.txt")
parser.add_argument('--outfile', help='Output json file containing metadata for all videos', default="/share/pi/cleemess/file-conversion-pipeline/rekall_metadata.json")

args = parser.parse_args()
basedir = args.basedir
file_list = args.file_list
outfile = args.outfile

# dump json output
with open(outfile, 'w') as file:
  print("Generating metadata from video files in: %s, file_list %s" % (basedir, file_list))
  video_files = []
  with open(file_list, 'r') as f:
    for line in f.readlines():
      line = line.strip()
      video_files.append((os.path.join(basedir, line), line))
  video_files = sorted(list(set(video_files)))
  absolute_paths = [
    vf[0] for vf in video_files
  ]
  print("%d video files in list." % len(video_files))
  meta = generate_video_metadata(absolute_paths)
  print("Found %d videos." % len(meta))
  print("Writing %s" % outfile)
  json.dump(meta, file)

  
