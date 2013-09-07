import csv

from litnetwork import config as cfg
from litnetwork import target_hugo as th
from collections import defaultdict
from IPython import embed

def convert_to_antibodies(source_file=None, dest_file=None):
    '''Processes reduced network file, replacing hugo id's with antibody id's.

    Further network reduction occurs in this step.
    Edges which map from the an antibody to itself are disallowed, and if there are
    multiple edges between antibody a and antibody b, the shortest edge with the best 
    score is the only one that is kept.
    '''
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
    '''Loads reduced network.'''
    with open(source_file) as f:
        reader = csv.reader(f, delimiter='\t')
        return [line for line in reader if '#' not in line[0]]

def make_substitutions(hugo_dict, source_net):
    '''Substitute Hugo Id's with corresponding antibody id's.
    
    Not a simple 1-1 substitution, as it is possible for a Hugo ID
    to map to multiple antibodies. Due to this, a new row is created for 
    every possible antibody mapping.
    '''
    result = []
    for line in source_net:
        sources = hugo_dict[line[0]]
        targets = hugo_dict[line[1]]
        result += [[source, target]+ line[2:] for source in sources for target in targets]
    return result

def merge_antibodies(network):
    '''Merge duplicate antibodies into one row.

    After hugo -> antibody substitutions occur, it is possible for duplicate
    source/target entries to exist. This method locates the duplicates,
    and selects the best entry that exists for that source/target pair.
    The best entry is path with the shortest path with the best score,
    with path length having priority.
    '''
    temp_dict = defaultdict(list)    
    for row in network:
        key = (row[0],row[1])
        value = row[2:]
        temp_dict[key].append(value)
    result_dict = {}
    for key in temp_dict:
        values = temp_dict[key]
        #sort by path length, then score
        sorted_paths = sorted(values,key = lambda x: (float(x[1]),-float(x[0])))
        result_dict[key] = sorted_paths[0]
    return [list(key)+result_dict[key] for key in result_dict]


def filter_illegal_links(network):
    '''Removes 'illegal' entries from network.
    
    Disallows entries where the same antibody is the source/target,
    and disallows non-phosphorylized entries ('_p' not in antibody name').
    '''
    result = []
    for row in network:
        if row[0] != row[1] and '_p' in row[0] and '_p' in row[1]:
            result.append(row)
    return result

if __name__=='__main__':
    convert_to_antibodies()

