import os
import csv

from IPython import embed
from litnetwork import cfg
from collections import defaultdict

#singleton containing data from file
data = None
def get_data():
    global data
    if not data:
        data = load_file()
    return data

def process_row(row):
    ids = row[1].split('_')[0].split('.')
    return row[0], ids

def load_file(in_file=None):
    if not in_file:
        in_file = cfg.target_hugo_file
    with open(in_file) as f:
        reader = csv.reader(f, delimiter='\t')
        return [process_row(line) for line in reader if line[3]!= '1'][1:]

def get_id_list():
    data = get_data()
    return [hid for entry in data for hid in entry[1]]

def get_ab_list():
    data = get_data()
    return [row[0] for row in data]

def get_hugo_to_antibody_dict():
    data = get_data()
    res = defaultdict(list)
    for entry in data:
        for hid in entry[1]:
            res[hid].append(entry[0])
    return res

