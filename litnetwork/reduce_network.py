import networkx as nx
import csv
from litnetwork import config as cfg

def reduce_network(source_file=None, dest_file=None, hugo_file=None, cutoff=2):
    if not source_file:
        source_file = cfg.compiled_data_file
    if not dest_file:
        dest_file = cfg.reduced_data_file
    if not hugo_file:
        hugo_file = cfg.target_hugo_file
    with open(hugo_file) as f:
        hugo_targets = [line.strip() for line in f]
    unfiltered_net = read_network(source_file)
    filter_network(unfiltered_net, cutoff, hugo_targets)


def read_network(source_file):
    with open(source_file) as f:
        reader = csv.reader(f, delimiter = '\t')
        entries = [line for line in reader if '#' not in line[0]]
    network = nx.DiGraph()
    for entry in entries:
        network.add_edge(entry[0],entry[1],score=entry[2], meta=entry[3:])
    return network 

def filter_network(unfiltered_network, cutoff, targets):
    permuations = [(first,second) for first in targets for second in targets if first != second]
    

    for pair in permuations:
        try:
            paths = nx.all_simple_paths(unfiltered_network, pair[0], pair[1], cutoff=cutoff)
            paths = [list(path) for path in paths]
            for path in paths:
                if len(path)>0:
                    print path
        except:
            pass

if __name__=='__main__':
    reduce_network()
