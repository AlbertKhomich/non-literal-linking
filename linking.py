import heapq
import pickle
import numpy as np
import faiss

output_similar_pairs_path = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/similar_pairs.txt'
entity_to_idx_path = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/entity_to_idx.p'
entity_embeddings_path = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/entity_embeddings.npy'

threshold = 0.25
k = 100
top_n = 100
n_threads = 64

with open(entity_to_idx_path, 'rb') as f:
    entity_to_idx = pickle.load(f)

entity_embeddings_np = np.load(entity_embeddings_path)
num_entities, dimension = entity_embeddings_np.shape

entity_embeddings_norm = entity_embeddings_np / np.linalg.norm(entity_embeddings_np, axis=1, keepdims=True)
entity_embeddings_norm = entity_embeddings_norm.astype(np.float32)

faiss.omp_set_num_threads(n_threads)

index = faiss.IndexHNSWFlat(dimension, 32, faiss.METRIC_INNER_PRODUCT)
index.hnsw.efConstruction = 40
index.hnsw.efSearch = 50

print("Adding embeddings to FAISS index...")
index.add(entity_embeddings_norm)

idx_to_entity = {v: k for k, v in entity_to_idx.items()}

print("Searching for similar pairs...")
distances, indices = index.search(entity_embeddings_norm, k)

max_heap = []

threshold_inner_product = threshold

for i in range(num_entities):
    e1_idx = i
    e1 = idx_to_entity[e1_idx]
    for j in range(k):
        neighbor_idx = indices[i][j]
        if neighbor_idx == e1_idx:
            continue
        if e1_idx < neighbor_idx:
            similarity = distances[i][j]
            if similarity >= threshold_inner_product:
                e2 = idx_to_entity[neighbor_idx]
                if len(max_heap) < top_n:
                    heapq.heappush(max_heap, (similarity, e1, e2))
                else:
                    if similarity > max_heap[0][0]:
                        heapq.heappushpop(max_heap, (similarity, e1, e2))

top_similar_pairs = heapq.nlargest(top_n, max_heap, key=lambda x: x[0])

print(f"Writing top {top_n} similar pairs to {output_similar_pairs_path}...")
with open(output_similar_pairs_path, 'w') as f:
    for sim, e1, e2 in top_similar_pairs:
        f.write(f"{sim:.4f}\t{e1}\t{e2}\n")

print("Completed successfully.")
