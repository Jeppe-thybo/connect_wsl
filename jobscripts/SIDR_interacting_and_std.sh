#!/bin/bash
#SBATCH --job-name=SIDR_interacting_and_std
#SBATCH --partition=qany
#SBATCH --mem-per-cpu=2g
#SBATCH --ntasks=36
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --output=SIDR_interacting_and_std.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jeppethybo@live.dk
echo "========= Job started at `date` =========="

cd /home/jthybo/connect_wsl/

# activate proper environment if needed
module load gcc openmpi

# source planck data (load path from connect.conf)
clik_line=$(grep -hr "clik" mcmc_plugin/connect.conf)
path_split=(${clik_line//= / })
path="$(echo ${path_split[1]} | sed "s/'//g")bin/clik_profile.sh"
source $path

python connect.py create input/SIDR_interacting_and_std.param

echo "========= Job finished at `date` =========="
