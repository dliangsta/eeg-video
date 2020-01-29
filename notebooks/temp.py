#!/usr/bin/env python
# coding: utf-8

# In[8]:


import json
from tqdm import tqdm
import os, os.path
from rekall import Interval, IntervalSet, IntervalSetMapping, Bounds3D
from vgrid import VGridSpec, VideoMetadata, VideoBlockFormat, FlatFormat
from vgrid import SpatialType_Keypoints, Metadata_Keypoints
from vgrid_jupyter import VGridWidget


# # Load metadata for videos
# 
# Read from `/media/4tb_hdd/shared/goodvideo_lpch/file_metadata.json`.

# In[7]:


VIDEO_DIR='/home/clee/code/eegml/data/goodvideo_lpch'

with open('/home/clee/code/eegml/data/goodvideo_lpch/video-metadata.json', 'r') as f:
    video_files = json.load(f)
    
print('There are {} videos with metadata'.format(len(video_files)))

metadata_videos = [
    VideoMetadata(
        v["filename"], id=v["id"], fps=v["fps"],
        num_frames=int(v["num_frames"]), width=v["width"], height=v["height"])
    for v in video_files
]


# # Load pose annotations

# In[20]:


pose_annotation_files = []
with open(os.path.join(VIDEO_DIR,'pose_annotation_list.txt'), 'r') as f:
    for line in f.readlines():
        pose_annotation_files.append(os.path.join(VIDEO_DIR,line.strip()))


# In[21]:


metadata_videos[0].path


# In[22]:


pose_annotation_files[0]


# In[23]:


def json_path_to_video_path(json_path):
    return os.path.join(
        os.path.basename(os.path.dirname(json_path)),
        os.path.basename(json_path)
    )[:-4]


# In[24]:


def video_path_to_vm(video_path):
    for vm in metadata_videos:
        if vm.path[:-3] == video_path:
            return vm
    return None


# In[25]:


def pose_annotation_to_array(pose_annotation):
    '''
    Assumes a format that looks like this for each frame:
    {
        '0': {'0': [0.5694444444444444, 0.5271739130434783]},
        '1': {'1': [0.4675925925925926, 0.7391304347826086]},
        '2': {'2': [0.2962962962962963, 0.7717391304347826]},
        '5': {'5': [0.6712962962962963, 0.6902173913043478]},
        '6': {'6': [0.7314814814814815, 0.9184782608695652]},
        '14': {'14': [0.5231481481481481, 0.45652173913043476]},
        '15': {'15': [0.6157407407407407, 0.483695652173913]},
        '16': {'16': [0.4027777777777778, 0.483695652173913]},
        '17': {'17': [0.6435185185185185, 0.5163043478260869]}
    }
    '''
    new_pose = []
    for i in range(18):
        if str(i) in pose:
            keypoint = pose[str(i)][str(i)]
            new_pose.append([keypoint[0], keypoint[1], 1])
        else:
            new_pose.append([0, 0, 0])
    return new_pose


# In[26]:


pose_metadata = {}
for pose_annotation_file in pose_annotation_files:
    pose_intervals = []
    with open(pose_annotation_file, 'r') as f:
        stride = 10
        pose_annotations = [
            json.loads(line.strip())
            for line in f.readlines()
        ][::stride]
        
        video_meta = video_path_to_vm(
            json_path_to_video_path(pose_annotation_file)
        )
        
        if video_meta is None:
            continue
        
        for frame_number, pose_annotation in tqdm(enumerate(pose_annotations), total=len(pose_annotations)):
            start = (frame_number * stride) / video_meta.fps
            end = (frame_number + 1) * stride / video_meta.fps
            for pose in pose_annotation:
                pose_intervals.append(
                    Interval(
                        Bounds3D(start, end),
                        {
                            'spatial_type': SpatialType_Keypoints(),
                            'metadata': {
                                'pose': Metadata_Keypoints.from_openpose(
                                    pose_annotation_to_array(pose)
                                )
                            }
                        }
                    )
                )
        
        pose_metadata[video_meta.id] = IntervalSet(pose_intervals)


# In[29]:


pose_annotation_files


# In[31]:


vgrid_spec = VGridSpec(
    video_meta = metadata_videos,
    vis_format = VideoBlockFormat(imaps = [
        ('pose', IntervalSetMapping(pose_metadata))
    ]),
    video_endpoint = 'http://localhost:8080'
)
VGridWidget(vgrid_spec = vgrid_spec.to_json_compressed())


# In[ ]:




