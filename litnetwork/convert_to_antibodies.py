import csv

from litnetwork import config as cfg
from litnetwork import target_hugo as th

def convert_to_antibodies(source_file=None, dest_file=None):
    if not source_file:
        source_file = cfg.reduced_data_file
    if not dest_file:
        dest_file = cfg.reduced_antibody_data_file
    hugo_ab_dict = th.get_hugo_to_antibody_dict()
    hugo_network = load_file(source_file)
    ab_network = make_substitutions(hugo_ab_dict, hugo_network)
    with open(dest_file, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['#source','target','score','length','meta'])
        writer.writerows(ab_network)
    
def load_file(source_file):
    with open(source_file) as f:
        reader = csv.reader(f, delimiter='\t')
        return [line for line in reader if '#' not in line[0]]

def make_substitutions(hugo_dict, source_net):
    result = []
    for line in source_net:
        sources = hugo_dict[line[0]]
        targets = hugo_dict[line[1]]
        result += [[source, target]+ line[2:] for source in sources for target in targets]
    return result
