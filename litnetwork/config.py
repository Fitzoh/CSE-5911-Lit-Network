import os.path
__all__ = ['pwd']

project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_root = os.path.join(project_root, 'data')
unprocessed_data_dir = os.path.join(data_root, 'unprocessed_sources')
processed_data_dir = os.path.join(data_root, 'processed_sources')
compiled_data_file = os.path.join(data_root, 'compiled_processed_sources.csv')
reduced_data_file = os.path.join(data_root, 'reduced_network.csv')
target_hugo_file = os.path.join(data_root, 'target_hugo.txt')
