#!/bin/bash
#SBATCH --job-name=DRMD_desi_iter_mcmc_2
#SBATCH --partition=qany
#SBATCH --mem-per-cpu=2g
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --output=DRMD_desi_iter_mcmc_2.out
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

cd resources/montepython_public/
srun --mpi=none --ntasks=4 --cpus-per-task=1 \
  python montepython/MontePython.py run \
  -p /home/jthybo/connect_wsl/mcmc_plugin/mp_param_templates/DRMD_desi_2.param \
  --conf /home/jthybo/connect_wsl/mcmc_plugin/connect.conf \
  --covmat /home/jthybo/connect_wsl/resources/montepython_public/covmat/DRMD_base_M.covmat \
  -o chains/DRMD_desi_iter_2 \
  --chain-number $SLURM_PROCID


echo "========= Job finished at `date` =========="
