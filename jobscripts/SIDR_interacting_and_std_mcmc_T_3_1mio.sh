#!/bin/bash
#SBATCH --job-name=SIDR_1mio
#SBATCH --partition=q64
#SBATCH --mem-per-cpu=3g
#SBATCH --ntasks=6
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --output=SIDR_interacting_and_std_mcmc_T_3_1mio.out
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

srun --mpi=none --ntasks=6 --cpus-per-task=1  \
  python montepython/MontePython.py run \
  -p /home/jthybo/connect_wsl/mcmc_plugin/mp_param_templates/SIDR_interacting_and_std_1mio.param \
  --conf /home/jthybo/connect_wsl/mcmc_plugin/connect.conf \
  --covmat /home/jthybo/connect_wsl/resources/montepython_public/covmat/base2018TTTEEE_lite.covmat \
  -T 3.0 \
  --silent \
  -o chains/SIDR_interacting_and_std_T_3_1mio

echo "========= Job finished at `date` =========="
