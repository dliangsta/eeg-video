import argparse
import glob
import json
import os
import shlex
import subprocess
import sys

def generate_video_metadata(absolute_paths, relative_paths):
    
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
    
    for absolute_path, relative_path in zip(absolute_paths, relative_paths):

        cmd = "ffprobe -v quiet -print_format json -show_streams %s" % absolute_path
        try:
            outp = subprocess.check_output(shlex.split(cmd)).decode("utf-8")
        except:
            print('Error on %', absolute_path)
            continue
        streams = json.loads(outp)["streams"]
        video_stream = [s for s in streams if s["codec_type"] == "video"][0]

        [num, denom] = map(int, video_stream["r_frame_rate"].split('/'))
        fps = float(num) / float(denom)
        num_frames = video_stream["nb_frames"]
        width = video_stream["width"]
        height = video_stream["height"]

        id = len(vids)
        
        meta = { "id" : id,
                 "filename" : relative_path,
                 "num_frames" : num_frames,
                 "fps" : fps,
                 "width" : width,
                 "height" : height}

        vids.append(meta)

    return vids



parser = argparse.ArgumentParser(description='Generate video metadata.')
parser.add_argument('basedir', help='Base directory containing videos')
parser.add_argument('file_list', help='List of video files')
parser.add_argument('outfile', help='Output json file containing metadata for all videos')

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
    relative_paths = [
        vf[1] for vf in video_files
    ]
    print("%d video files in list." % len(video_files))
    meta = generate_video_metadata(absolute_paths, relative_paths)
    print("Found %d videos." % len(meta))
    print("Writing %s" % outfile)
    json.dump(meta, file)

    
