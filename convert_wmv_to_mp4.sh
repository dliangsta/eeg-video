#!/bin/bash
#
#SBATCH --job-name=convert_wmv_to_mp4
#
#SBATCH --time=2880
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=8G

module load anaconda
source activate /share/pi/cleemess/envs/eeg1

srun python convert_wmv_to_mp4.py