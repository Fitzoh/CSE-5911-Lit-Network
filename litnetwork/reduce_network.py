import networkx as nx
import csv
from litnetwork import config as cfg

def reduce_network(source_file=None, dest_file=None, hugo_file=None, cutoff=3):
    if not source_file:
        source_file = cfg.compiled_data_file
    if not dest_file:
        dest_file = cfg.reduced_data_file
    if not hugo_file:
        hugo_file = cfg.target_hugo_file
    with open(hugo_file) as f:
        hugo_targets = [line.strip() for line in f]
    unfiltered_net = read_network(source_file)
    filtered_data = filter_network(unfiltered_net, cutoff, hugo_targets)
    with open(cfg.reduced_data_file, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['source','target','score','length','meta'])
        writer.writerows(filtered_data)


def read_network(source_file):
    with open(source_file) as f:
        reader = csv.reader(f, delimiter = '\t')
        entries = [line for line in reader if '#' not in line[0]]
    network = nx.DiGraph()
    for entry in entries:
        network.add_edge(entry[0],entry[1],score=float(entry[2]), meta=entry[3:])
    return network

def filter_network(unfiltered_network, cutoff, targets):
    permuations = [(first,second) for first in targets for second in targets if first != second]
    reduced = nx.DiGraph()
    data = []
    for pair in permuations:
        row = find_path(unfiltered_network, pair[0],pair[1], cutoff)
        if row:
            data.append(row)
    return data

def find_path(network, source, target, cutoff):
    for i in range(cutoff):
        try:
            paths = nx.all_simple_paths(network, source, target, i + 1)
            paths = [list(path) for path in paths]
            if paths:
                return best_path(network, paths)
        except:
            pass
    return None


def best_path(network, paths):
    sorted_paths = sorted(paths, key = lambda path: -1*get_confidence(network, path))
    best_path = sorted_paths[0]
    source = best_path[0]
    target = best_path[-1]
    score = get_confidence(network, best_path)
    length = len(best_path)-1
    #TODO modify meta entry w/ more info
    meta = str(best_path)
    return [source, target, score, length, meta]

def get_confidence(network, path):
    score  = 1
    for i in range(len(path)-1):
        score *= network[path[i]][path[i+1]]['score']
    return score
    #print path

if __name__=='__main__':
    reduce_network()
