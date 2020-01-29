#!/bin/bash
#
#SBATCH --job-name=generate_video_metadata
#
#SBATCH --time=1000:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=32G

module load anaconda
source activate /share/pi/cleemess/envs/eeg1
cd /share/pi/cleemess/eeg-summaries/good_video_lpch/
echo "Creating /share/pi/cleemess/eeg-summaries/mp4s.txt"
date
find */*/*.mp4 > /share/pi/cleemess/eeg-summaries/mp4s.txt
echo "Finished creating /share/pi/cleemess/eeg-summaries/mp4s.txt"
date
echo "Creating video metadata"
cd ~/nk_database_proj/eeg-video
python create_video_metadata.py
date