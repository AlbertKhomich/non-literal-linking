"""
This script finds and stores the top similar entity pairs based on their embeddings.

It utilizes the FAISS library for efficient similarity search in high-dimensional space. The key steps involved are:

1. Load entity-to-index mappings and embeddings from files.
2. Normalize the embeddings.
3. Set up a FAISS index for fast nearest neighbor search using the HNSW algorithm.
4. Search for the nearest neighbors of each entity while avoiding duplicates.
5. Store pairs that exceed a specified similarity threshold in a max heap.
6. Write the top similar pairs to an output file.

Parameters:
- threshold: Minimum similarity score for a pair to be considered similar.
- k: Number of nearest neighbors to retrieve for each entity.
- top_n: Number of top similar pairs to output.
- n_threads: Number of threads for parallel processing.
"""

import argparse
import heapq
import pickle
import numpy as np
import os
import faiss
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def load_entity_to_idx(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.csv':
        logging.info(f"Loading entity-to-index mapping from CSV file: {file_path}")
        df = pd.read_csv(file_path)
        entity_to_idx = {entity: idx for idx, entity in enumerate(df['entity'])}
    
    elif file_extension == '.p' or file_extension == '.pickle':
        logging.info(f"Loading entity-to-index mapping from Pickle file: {file_path}")
        with open(file_path, 'rb') as f:
            entity_to_idx = pickle.load(f)

    else:
        logging.error(f"Unsupported file format: {file_extension}")
        raise ValueError(f"Unsupported file format: {file_extension}")

    return entity_to_idx

parser = argparse.ArgumentParser(description='Find and store top similar entity pairs based on embeddings.')
parser.add_argument('--output_similar_pairs_path', type=str, required=True, help='Path to the output file for similar pairs.')
parser.add_argument('--entity_to_idx_path', type=str, required=True, help='Path to the entity-to-index mapping file.')
parser.add_argument('--entity_embeddings_path', type=str, required=True, help='Path to the entity embeddings file.')
parser.add_argument('--threshold', type=float, default=0.25, help='Minimum similarity score for a pair to be considered similar.')
parser.add_argument('--k', type=int, default=100, help='Number of nearest neighbours to retrieve for each entity')
parser.add_argument('--top_n', type=int, default=100, help='Number of top similar pairs to output.')
parser.add_argument('--n_threads', type=int, default=126, help='Number of threads for parallel processing.')

args = parser.parse_args()

index_file_path="faiss_index.index"

entity_to_idx = load_entity_to_idx(args.entity_to_idx_path)

entity_embeddings_np = np.load(args.entity_embeddings_path)
num_entities, dimension = entity_embeddings_np.shape

logging.info(f"Normalizing {num_entities} embeddings...")
entity_embeddings_norm = entity_embeddings_np / np.linalg.norm(entity_embeddings_np, axis=1, keepdims=True)
entity_embeddings_norm = entity_embeddings_norm.astype(np.float32)

idx_to_entity = {v: k for k, v in entity_to_idx.items()}

faiss.omp_set_num_threads(args.n_threads)

if os.path.exists(index_file_path):
    logging.info("Loading FAISS index from cache...")
    index = faiss.read_index(index_file_path)
else:
    logging.info(f"Creating a new FAISS index with dimension {dimension}...")
    index = faiss.IndexHNSWFlat(dimension, 32, faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efConstruction = 40
    index.hnsw.efSearch = 50
    index.add(entity_embeddings_norm)    
    logging.info("Saving FAISS index to cache...")
    faiss.write_index(index, index_file_path)

logging.info("Searching for similar pairs...")
distances, indices = index.search(entity_embeddings_norm, args.k)

max_heap = []
all_valid_pairs = []

threshold_inner_product = args.threshold

for i in range(num_entities):
    e1_idx = i
    e1 = idx_to_entity[e1_idx]
    for j in range(args.k):
        neighbor_idx = indices[i][j]
        if neighbor_idx == e1_idx:
            continue
        if e1_idx < neighbor_idx:
            similarity = distances[i][j]
            all_valid_pairs.append((similarity, e1, idx_to_entity[neighbor_idx]))
            if similarity >= threshold_inner_product:
                e2 = idx_to_entity[neighbor_idx]
                if len(max_heap) < args.top_n:
                    heapq.heappush(max_heap, (similarity, e1, e2))
                else:
                    if similarity > max_heap[0][0]:
                        heapq.heappushpop(max_heap, (similarity, e1, e2))

logging.info(f"Total valid similarities found: {len(all_valid_pairs)}")

top_similar_pairs = heapq.nlargest(args.top_n, max_heap, key=lambda x: x[0])

logging.info(f"Writing all valid similar pairs to {args.output_similar_pairs_path}...")
with open(args.output_similar_pairs_path, 'w') as f:
    for sim, e1, e2 in all_valid_pairs:
        f.write(f"{sim:.4f}\t{e1}\t{e2}\n".strip('<>'))

logging.info("Completed successfully.")

# print(f"Writing top {args.top_n} similar pairs to {args.output_similar_pairs_path}...")
# with open(args.output_similar_pairs_path, 'w') as f:
#     for sim, e1, e2 in top_similar_pairs:
#         f.write(f"{sim:.4f}\t{e1}\t{e2}\n".strip('<>'))

# print("Completed successfully.")
