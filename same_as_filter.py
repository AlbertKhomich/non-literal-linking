import argparse
import csv

parser = argparse.ArgumentParser(description='Find similar pairs with sameAs relationships.')
parser.add_argument('--input_path_alignment', type=str, required=True, help='Path to the same_as.nt file.')
parser.add_argument('--input_path_similar_pairs', type=str, required=True, help='Path to the similar pairs.txt file.')
parser.add_argument('--input_path_classes_1', type=str, required=True, help='Path to the classes_1.nt file.')
parser.add_argument('--input_path_classes_2', type=str, required=True, help='Path to the classes_2.nt file.')
parser.add_argument('--input_path_props_1', type=str, required=True, help='Path to the props_1.nt file.')
parser.add_argument('--input_path_props_2', type=str, required=True, help='Path to the props_2.nt file.')
parser.add_argument('--output_file', type=str, required=True, help='Path to the output CSV file.')

args = parser.parse_args()

existing_same_as = set()
same_as_pair = []
dataset1 = {}
dataset2 = {}

# input_path_alignment = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/same_as.nt'
# input_path_similar_pairs = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/similar_pairs_0_25.txt'
# input_path_classes_1 = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/bioportal_classes.nt'
# input_path_classes_2 = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/go_classes.nt'
# input_path_props_1 = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/bioportal_properties_correct.nt'
# input_path_props_2 = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/go_properties_correct.nt'
# output_file = '/scratch/hpc-prf-lola/albert/non_literal_linking/data/Keci_GPU_bioportal_GO_dataset_1/similar_pairs_same_as.csv'

with open(args.input_path_classes_1, 'r') as cl1:
    for c in cl1:
        triple = c.strip().split('\t')
        uri = triple[0]
        label = triple[2]
        dataset1[uri] = label

with open(args.input_path_props_1, 'r') as pr1:
    for c in pr1:
        triple = c.strip().split('\t')
        uri = triple[0]
        label = triple[2]
        dataset1[uri] = label

with open(args.input_path_classes_2, 'r') as cl2:
    for c in cl2:
        triple = c.strip().split('\t')
        uri = triple[0]
        label = triple[2]
        dataset1[uri] = label

with open(args.input_path_props_2, 'r') as pr2:
    for c in pr2:
        triple = c.strip().split('\t')
        uri = triple[0]
        label = triple[2]
        dataset1[uri] = label

with open(args.input_path_alignment, 'r') as file:
    for line in file:
        triple = line.strip().split(' ')
        e1 = triple[0]
        e2 = triple[2]
        existing_same_as.add((e1 + dataset1[e1] + e2 + dataset1[e2]))

with open(args.input_path_similar_pairs, 'r') as f:
    for l in f:
        t = l.strip().split('\t')
        sim = t[0]
        en1 = t[1]
        en2 = t[2]
        for arr in existing_same_as:
            if en1 in arr and en2 in arr:
                same_as_pair.append((sim, en1, en2))

with open(args.output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Similarity', 'Entity 1', 'Entity 2'])
    if same_as_pair:
        writer.writerows(same_as_pair)
    else:
        writer.writerow(['No sameAs found.','',''])
