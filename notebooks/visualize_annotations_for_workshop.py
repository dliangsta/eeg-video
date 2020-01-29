# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import json
import os
assert os.environ["CONDA_DEFAULT_ENV"] == "rekall"

from tqdm import tqdm
from glob import glob

BASE_DIR = "/share/pi/cleemess/eeg-summaries/good_video_lpch/"

# # Read metadata

# We read in the video metadata.

with open('/share/pi/cleemess/eeg-summaries/metadata.json') as f:
    video_metadata = list(json.load(f))
video_metadata[0]


video_metadata = [vm for vm in video_metadata if vm['filename'].split("/")[0] in ['BA12305R', 'BA12306N']]
video_metadata

video_metadata[0]['filename'].split("/")

for vm in video_metadata:
    fn = vm["filename"]
    json_fn = os.path.join(BASE_DIR, fn.replace(".mp4", ".json"))
    print(fn, json_fn, os.path.isfile(json_fn))
    lines = {}
    with open(json_fn) as f:
        for i, line in tqdm(enumerate(list(f.readlines()))):
            line = json.loads(line)
            if len(line):
                lines[i] = line
                prev_line = line
    print(lines)
    print(i)
    break
#     print(new_fn)
#     print(vm["filename"], os.listdir("/share/pi/cleemess/eeg-summaries/good_video_lpch/" + vm['filename'].split("/")[0] + "/VOR"))

print('There are {} videos with metadata'.format(len(video_metadata)))

# # Filter videos

from glob import glob
import eeghdf

# Filter out videos that we can't find the annotation file for:

# +
annotation_exists_count = 0
for i, vm in enumerate(video_metadata):
#     print(vm)
    # Convert video filename to annotation filename
    vm["filename"] = vm["filename"].replace("stanford/","")
    fn = vm["filename"]
    intermediate = fn.split("/")[-1]
    num = int(intermediate[-6:-4])
    parent = "/".join(fn.split("/")[:-2])
    img_folder = fn.split("/")[-2][:-4]
    annotation_file = img_folder + f"_1-{num+1}+.eeg.h5"
    full_fn = os.path.join("/share/pi/cleemess/eeg-summaries/good_video_lpch/", parent, f"{parent}{annotation_file}")
#     if not os.path.isfile(full_fn):
#         print(fn, full_fn, os.path.isfile(full_fn))
    
    vm["annotation_filename"] = full_fn if os.path.exists(full_fn) else None
    annotation_exists_count += int(os.path.exists(full_fn))
    
print(f"We found annotations for {annotation_exists_count} of the {len(video_metadata)} videos.")
# -

# Now filter out videos that aren't broken up into pieces because we aren't totally sure how they line back up together.

only_video_count = 0
for vm in video_metadata:
    fn = vm["filename"]
    parent = os.path.join("/share/pi/cleemess/eeg-summariees", "/".join(fn.split("/")[:-1]))
    fn = fn.split("/")[-1]
    other_vids = glob(os.path.join(parent, fn[:-6]) + "*.mp4")
    vm["only_video"] = len(other_vids) == 1
    only_video_count += int(len(other_vids) == 1)
print(f"{only_video_count} of the {len(video_metadata)} videos are the only video in their directory (so this video is not a part of a sequence of broken up clips).")

# Then we find out the number of videos we can actually work with.

count = 0
for vm in video_metadata:
    count += int(vm["only_video"] and vm["annotation_filename"] is not None)
print(f"{count} of the {len(video_metadata)} videos are both the only video in their directory and have annotations.")

# # Visualize videos with annotations

from vgrid import VGridSpec, VideoMetadata, VideoBlockFormat, SpatialType_Caption
from vgrid_jupyter import VGridWidget
from rekall import Interval, IntervalSet, IntervalSetMapping, Bounds3D

# We wrap the video metadata in a special object for use in VGrid.

video_metadata_wrapper = [
    VideoMetadata(
        vm["filename"], id=str(id), fps=vm["fps"],
        num_frames=int(vm["num_frames"]), width=vm["width"], height=vm["height"])
    for id, vm in enumerate(video_metadata)
]


# Finally, we create a  function that filters the videos for annotations that contain the keyword.

def find_clips_for_keyword(keyword, use_only_video=False):
    ism = {}
    for vm in tqdm(video_metadata):
        if not vm["annotation_filename"] or (not vm["only_video"] and use_only_video):
            continue
        try:
            h5 = eeghdf.Eeghdf(vm["annotation_filename"])
        except:
            print(vm["annotation_filename"])
            os.remove(vm["annotation_filename"])
            continue
        starts = [start / 10**7 for start in h5._annotation_start100ns]
        texts = h5._annotation_text

        if not keyword or any(keyword.lower() in text.lower() for text in texts):
            interval_set = IntervalSet([
                    Interval(
                        Bounds3D(start , start + 5), # we set the duration
                        {
                            'spatial_type': SpatialType_Caption(">>" + text + "\n"),
                            'metadata': {}
                        }
                    ) for start, text in zip(starts, texts)
                ]) 
            ism[vm["id"]] = interval_set

    print(f"Found {len(ism)} videos with keyword {keyword} in the annotations.")
    vgrid_spec = VGridSpec(
        video_meta=video_metadata_wrapper,
        vis_format=VideoBlockFormat(imaps=[('bboxes', ism)]),
        video_endpoint='http://localhost:8080'
    )
    return VGridWidget(vgrid_spec=vgrid_spec.to_json_compressed())


# Then we use the function to visualize clips with seizures.

find_clips_for_keyword("seizure")

find_clips_for_keyword("patting")

# ## Observations

# Some of the videos are not as good, but the first video clearly shows a seizure at the annotation's time stamp. 
#
# The final video also shows a seizure at the 9:40 mark, not where the annotation start time marker is though.
#
# The other videos don't seem like seizures to me but I am by no means an expert.
