import os
import csv

from IPython import embed
from litnetwork import cfg
from collections import defaultdict

#singleton containing data from file
data = None
def get_data():
    '''Loads data file if data singleton has not yet been initialized.'''
    global data
    if not data:
        data = load_file()
    return data

def process_row(row):
    '''Splits row into Hugo Id's.
    
    Rows are of the form "ID_ID.etc"
    Information after the period is discarded.
    '''
    ids = row[1].split('_')[0].split('.')
    return row[0], ids

def load_file(in_file=None):
    '''Load Hugo/Antibody file, discarding header and 'bad' entries.'''
    if not in_file:
        in_file = cfg.target_hugo_file
    with open(in_file) as f:
        reader = csv.reader(f, delimiter='\t')
        #if line[3]=='1', it is a bad entry and should be discarded
        return [process_row(line) for line in reader if line[3]!= '1'][1:]

def get_id_list():
    '''Returns list of Hugo id's.'''
    data = get_data()
    return [hid for entry in data for hid in entry[1]]

def get_ab_list():
    '''Returns list of antibodies.'''
    data = get_data()
    return [row[0] for row in data]

def get_hugo_to_antibody_dict():
    '''Returns dictionary mapping Hugo id's to corresponding antibodies.'''
    data = get_data()
    res = defaultdict(list)
    for entry in data:
        for hid in entry[1]:
            res[hid].append(entry[0])
    return res

