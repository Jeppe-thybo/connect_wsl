#!/bin/bash

# Define the folder where your code lives
WORKDIR="/home/jeppethybo/connect_public"

# Move to that folder
cd "$WORKDIR" || { echo "Folder not found: $WORKDIR"; exit 1; }
echo "Current working directory: $(pwd)"

#Run your neural network training script
echo "Starting neural networkcreation..."
python connect.py create input/LCDM-hyper.param

# Train your NN
echo "Starting neural network training..."
python connect.py train input/LCDM-hyper.param

#Move to new folder for MCMC analysis
cd /home/jeppethybo/connect_public/resources/montepython_public/
rm -rf chains/lcdm-hyper

for i in {1..4}; do
    echo "Starting MCMC run #$i"
    time python montepython/MontePython.py run -p /home/jeppethybo/connect_public/mcmc_plugin/mp_param_templates/LCDM-hyper.param --conf /home/jeppethybo/connect_public/mcmc_plugin/connect.conf --covmat /home/jeppethybo/connect_public/resources/montepython_public/covmat/base2018TTTEEE_lensing_bao.covmat -o chains/lcdm-hyper > output_1.log 2>&1 &
done

wait
echo "All finished"
