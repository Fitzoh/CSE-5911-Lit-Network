import os.path
__all__ = ['pwd']

#root project directories
project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_root = os.path.join(project_root, 'data')

#csv file containing antibody-hugo id mapping
target_hugo_file = os.path.join(data_root, 'proteins_per_cell_line.csv')

#contains initial data files and cleaned versions
unprocessed_data_dir = os.path.join(data_root, 'unprocessed_sources')
processed_data_dir = os.path.join(data_root, 'processed_sources')

#intermediate data files
compiled_data_file = os.path.join(data_root, 'compiled_processed_sources.tab')
reduced_data_file = os.path.join(data_root, 'reduced_network.tab')
reduced_antibody_data_file = os.path.join(data_root, 'reduced_antibody_network.tab')

#final output matrix files
length_matrix_file = os.path.join(data_root, 'compiled_network_lengths_adj.tab')
score_matrix_file = os.path.join(data_root, 'compiled_network_score_adj.tab')
