#!/bin/bash
#
#SBATCH --job-name=run_http_server
#
#SBATCH --time=1000:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=32G

module load anaconda
# source activate /share/pi/cleemess/envs/rekall
source activate /home/dwliang/.conda/envs/rekall

cat /etc/hosts
cd /home/dwliang/nk_database_proj/eeg-video/notebooks
# jupyter notebook --ip=0.0.0.0 --no-browser --NotebookApp.iopub_data_rate_limit=1e10
jupyter notebook --ip=0.0.0.0 --no-browser #--NotebookApp.iopub_data_rate_limit=1e10
