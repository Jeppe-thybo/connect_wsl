#!/bin/bash
#SBATCH --job-name=SIDR_T_10_iter
#SBATCH --partition=qany
#SBATCH --mem-per-cpu=2g
#SBATCH --nodes=1
#SBATCH --ntasks=36
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --output=SIDR_T_10_iter.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jeppethybo@live.dk

echo "========= Job started at `date` =========="

cd /home/jthybo/connect_wsl/

# Set the number of tasks explicitly so Python can use it
export SLURM_NPROCS=36
export SLURM_CPUS_PER_TASK=1

# activate proper environment if needed
module load gcc openmpi

# source planck data
clik_line=$(grep -hr "clik" mcmc_plugin/connect.conf)
path_split=(${clik_line//= / })
path="$(echo ${path_split[1]} | sed "s/'//g")bin/clik_profile.sh"
source $path

# Run the CONNECT creation step
python connect.py create input/SIDR_T_10_iter.param

echo "========= Job finished at `date` =========="

