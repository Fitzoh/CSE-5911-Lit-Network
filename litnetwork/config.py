import os.path
__all__ = ['pwd']

project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_root = os.path.join(project_root, 'data')

target_hugo_file = os.path.join(data_root, 'proteins_per_cell_line.csv')

unprocessed_data_dir = os.path.join(data_root, 'unprocessed_sources')
processed_data_dir = os.path.join(data_root, 'processed_sources')

compiled_data_file = os.path.join(data_root, 'compiled_processed_sources.tab')
reduced_data_file = os.path.join(data_root, 'reduced_network.tab')
reduced_antibody_data_file = os.path.join(data_root, 'reduced_antibody_network.tab')


length_matrix_file = os.path.join(data_root, 'compiled_network_lengths_adj.tab')
score_matrix_file = os.path.join(data_root, 'compiled_network_score_adj.tab')
