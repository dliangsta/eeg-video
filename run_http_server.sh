#!/bin/bash
#
#SBATCH --job-name=run_http_server
#
#SBATCH --time=1000:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=32G

module load anaconda
source activate /share/pi/cleemess/envs/rekall

# cd /share/pi/cleemess/stanford-eeg-box
cd /share/pi/cleemess/file-conversion-pipeline
cat /etc/hosts
http-server
