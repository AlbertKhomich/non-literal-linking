import torch
import numpy as np

model_path = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/model.pt'
model = torch.load(model_path, map_location=torch.device('cpu'))

entity_embeddings = model['entity_embeddings.weight']
relation_embeddings = model['relation_embeddings.weight']

entity_embeddings_np = entity_embeddings.detach().cpu().numpy()
relation_embeddings_np = relation_embeddings.detach().cpu().numpy()

np.save('/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/entity_embeddings.npy', entity_embeddings_np)
np.save('/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/relation_embeddings.npy', relation_embeddings_np)

print('Entity and relation embeddings have been saved!')