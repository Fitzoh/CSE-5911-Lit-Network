import networkx as nx
import csv
from litnetwork import config as cfg
from litnetwork import target_hugo as th

def reduce_network(source_file=None, dest_file=None, cutoff=3):
    '''Reduces compiled network to list of paths between hugo id's of interest.
    
    Searches for paths between all target id's, with a maximum path length of cutoff.
    Only one path between any source/target pair will exist in the output file.
    If multiple paths exist, the shortest path will be taken.
    If multiple paths share the same shortest length, the path with the highest
    score will be taken.'''
    if not source_file:
        source_file = cfg.compiled_data_file
    if not dest_file:
        dest_file = cfg.reduced_data_file
    hugo_targets = th.get_id_list()
    unfiltered_net = read_network(source_file)
    filtered_data = filter_network(unfiltered_net, cutoff, hugo_targets)
    with open(dest_file, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['#source','target','score','length','meta'])
        writer.writerows(filtered_data)


def read_network(source_file):
    '''Reads initial compiled network and returns networkxgraph.
    
    Score and Metadata are attached as edge metadata.'''
    with open(source_file) as f:
        reader = csv.reader(f, delimiter = '\t')
        entries = [line for line in reader if '#' not in line[0]]
    network = nx.DiGraph()
    for entry in entries:
        network.add_edge(entry[0],entry[1],score=float(entry[2]), meta=entry[3:])
    return network

def filter_network(unfiltered_network, cutoff, targets):
    '''Performs network filtering of initial network.
    
    Finds all paths betwen target id's of length < cutoff.
    Returns reduced network as list of lists.'''
    permutations = [(first,second) for first in targets for second in targets if first != second]
    data = []
    for pair in permutations:
        row = find_path(unfiltered_network, pair[0],pair[1], cutoff, targets)
        if row:
            data.append(row)
    return data

def find_path(network, source, target, cutoff, hugo_targets):
    '''Returns the best path between source and target if it exists.
    
    Maximum path length of cutoff.
    While source and target must be on the list of target id's,
    any intermediate nodes must NOT be on the target id list.
    '''
    #incrementally increase path length until path is found or cutoff is reached
    for i in range(cutoff):
        try:
            #generate all paths between source/target w/ cutoff i
            paths = nx.all_simple_paths(network, source, target, i + 1)
            paths = [list(path) for path in paths]
            #filter out illegal paths
            paths = [path for path in paths if is_legal_path(path, hugo_targets)]
            #if anything passes filter, return best path
            if paths:
                return best_path(network, paths)
        except:
            pass
    return None

def is_legal_path(path, hugo_targets):
    '''Checks if any intermediate nodes are on target id list.

    If they are, this is an illegal path.
    '''
    intermediate_nodes = path[1:-1]
    return set(intermediate_nodes).isdisjoint(set(hugo_targets))

def best_path(network, paths):
    '''Returns path with best score among list of equal length paths.'''
    #sort by confidence score of path
    sorted_paths = sorted(paths, key = lambda path: -1*get_confidence(network, path))
    #best path is first entry, acquire data related to path and return it
    best_path = sorted_paths[0]
    source = best_path[0]
    target = best_path[-1]
    score = get_confidence(network, best_path)
    length = len(best_path)-1
    meta = str(best_path)
    return [source, target, score, length, meta]

def get_confidence(network, path):
    '''Calculates a confidence score for a path.
    
    Final score = 1*S1*S2...Sn for each score S on path'''
    score  = 1
    for i in range(len(path)-1):
        score *= network[path[i]][path[i+1]]['score']
    return score

if __name__=='__main__':
    reduce_network()
