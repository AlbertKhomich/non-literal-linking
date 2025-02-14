import torch
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Extract entity and relation embeddings from a PyTorch model.')
parser.add_argument('--model_path', type=str, required=True, help='Path to the model (.pt) file.')
parser.add_argument('--output_dir', type=str, required=True, help='Directory to save embeddings.')

args = parser.parse_args()

model = torch.load(args.model_path, map_location=torch.device('cpu'))

entity_embeddings = model['entity_embeddings.weight']
relation_embeddings = model['relation_embeddings.weight']

entity_embeddings_np = entity_embeddings.detach().cpu().numpy()
relation_embeddings_np = relation_embeddings.detach().cpu().numpy()

np.save(f'{args.output_dir}/entity_embeddings.npy', entity_embeddings_np)
np.save(f'{args.output_dir}/relation_embeddings.npy', relation_embeddings_np)

print('Entity and relation embeddings have been saved!')