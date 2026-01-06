#!/bin/bash
#SBATCH --job-name=DRMD_desi
#SBATCH --partition=qany
#SBATCH --mem-per-cpu=2g
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --output=DRMD_desi_%j.out
echo "========= Job started at `date` =========="

# activate proper environment if needed
module load gcc openmpi

# source planck data (load path from connect.conf)
clik_line=$(grep -hr "clik" mcmc_plugin/connect.conf)
path_split=(${clik_line//= / })
path="$(echo ${path_split[1]} | sed "s/'//g")bin/clik_profile.sh"
source $path

python connect.py create input/DRMD_desi.param

echo "========= Job finished at `date` =========="
