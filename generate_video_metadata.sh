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

python create_video_metadata.py