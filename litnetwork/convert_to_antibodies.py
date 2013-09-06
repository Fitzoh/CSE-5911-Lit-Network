import csv

from litnetwork import config as cfg
from litnetwork import target_hugo as th
from collections import defaultdict
from IPython import embed

def convert_to_antibodies(source_file=None, dest_file=None):
    if not source_file:
        source_file = cfg.reduced_data_file
    if not dest_file:
        dest_file = cfg.reduced_antibody_data_file
    hugo_ab_dict = th.get_hugo_to_antibody_dict()
    hugo_network = load_file(source_file)
    ab_network = make_substitutions(hugo_ab_dict, hugo_network)
    merged_net = merge_antibodies(ab_network)
    filtered_ab_net = filter_illegal_links(merged_net)
    with open(dest_file, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['#source','target','score','length','meta'])
        writer.writerows(filtered_ab_net)
    
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

def merge_antibodies(network):
    temp_dict = defaultdict(list)    
    for row in network:
        key = (row[0],row[1])
        value = row[2:]
        temp_dict[key].append(value)
    result_dict = {}
    for key in temp_dict:
        values = temp_dict[key]
        sorted_paths = sorted(values,key = lambda x: (float(x[1]),-float(x[0])))
        result_dict[key] = sorted_paths[0]
    return [list(key)+result_dict[key] for key in result_dict]


def filter_illegal_links(network):
    result = []
    for row in network:
        if row[0] != row[1] and '_p' in row[0] and '_p' in row[1]:
            result.append(row)
    return result


convert_to_antibodies()
