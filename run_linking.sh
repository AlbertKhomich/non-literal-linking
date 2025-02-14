#!/bin/bash
#SBATCH --job-name=emb_linking
#SBATCH --output=/scratch/hpc-prf-whale/albert/non_literal_linking/logs/output_%A_%a.log
#SBATCH --error=/scratch/hpc-prf-whale/albert/non_literal_linking/logs/error_%A_%a.log
#SBATCH --time=21-00:00:00
#SBATCH --partition=normal
#SBATCH -A hpc-prf-whale
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=akhomich@mail.uni-paderborn.de 

source /scratch/hpc-prf-whale/albert/non_literal_linking/venv/bin/activate

python3 /scratch/hpc-prf-whale/albert/non_literal_linking/src/linking.py \
--output_similar_pairs_path=/scratch/hpc-prf-whale/bio2rdf/embeddings/TransE_GPU_bioportal_SGD_sparql/2025-02-12_11-31-00.128337/similar_pairs.nt \
--entity_to_idx_path=/scratch/hpc-prf-whale/bio2rdf/embeddings/TransE_GPU_bioportal_SGD_sparql/2025-02-12_11-31-00.128337/entity_to_idx.csv \
--entity_embeddings_path=/scratch/hpc-prf-whale/bio2rdf/embeddings/TransE_GPU_bioportal_SGD_sparql/2025-02-12_11-31-00.128337/entity_embeddings.npy \
--threshold=0.7
