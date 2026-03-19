#!/bin/bash
#SBATCH --job-name=SIDR_test
#SBATCH --partition=q48
#SBATCH --mem-per-cpu=3g
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --output=SIDR_likelihood_test_mcmc.out
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

srun python montepython/MontePython.py run \
  -p /home/jthybo/connect_wsl/mcmc_plugin/mp_param_templates/SIDR_likelihood_test.param \
  --conf /home/jthybo/connect_wsl/mcmc_plugin/connect.conf \
  --covmat /home/jthybo/connect_wsl/resources/montepython_public/covmat/base2018TTTEEE_lite.covmat \
  -T 3.0 \
  --silent \
  -o chains/SIDR_likelihood_test \
  --chain-number 1 \

echo "========= Job finished at `date` =========="
