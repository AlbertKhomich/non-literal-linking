#!/bin/bash
#SBATCH --job-name=linking
#SBATCH --output=/scratch/hpc-prf-lola/albert/non_literal_linking/logs/linking.out
#SBATCH --error=/scratch/hpc-prf-lola/albert/non_literal_linking/logs/linking.err
#SBATCH --time=504:00:00
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=akhomich@mail.uni-paderborn.de 

source /scratch/hpc-prf-lola/albert/non_literal_linking/venv/bin/activate

python3 /scratch/hpc-prf-lola/albert/non_literal_linking/src/linking.py
