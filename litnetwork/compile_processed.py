from litnetwork import config as cfg
from collections import defaultdict
import operator
import os
import csv


def compile_all(source_dir=None, dest_file=None):
    '''Processes all cleaned data files and combines them in to one condensed file.'''
    if not source_dir:
        source_dir = cfg.processed_data_dir
    if not dest_file:
        dest_file = cfg.compiled_data_file
    score_dict = defaultdict(list)
    meta_dict = defaultdict(list)
    for path in os.listdir(source_dir):
        parse_file(os.path.join(source_dir, path), score_dict, meta_dict)
    processed_rows = process_rows(score_dict, meta_dict)
    write_file(dest_file, processed_rows)


def write_file(dest_file, rows):
    '''Write tab sep file to selected output file.'''
    meta_cols = max(map(len, rows)) - 3
    headers = ['#source', 'target', 'score'] + ['meta' + str(i) for i in range(meta_cols)]
    with open(dest_file, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(headers)
        writer.writerows(rows)


def parse_file(source_file, score_dict, meta_dict):
    '''Read one cleaned file, adding data to score/meta dict as it goes.
    
    Each dict uses the source/target tuple as the key.
    The values for score dict are the list of scores, for each source/target pair,
    with each file possibly contributing a score.
    The value for meta dict is the list of source file names that have contributed 
    a score for the source/target pair.
    '''
    with open(source_file) as f:
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            #filter out comment lines
            if '#' not in line[0]:
                key = (line[0], line[1])
                score_dict[key].append(float(line[2]))
                meta_dict[key].append(os.path.basename(source_file))


def process_rows(score_dict, meta_dict):
    '''Post processing once all files have been read.'''
    result_list = []
    for key in score_dict:
        #Final score = function of initial scores S1,S2,...,Sn
        #1-(1-S1)*(1-S2)*...*(1-Sn)
        score = 1 - reduce(operator.mul, map(lambda x: 1-x, score_dict[key]))
        result_list.append(list(key) + [score] + meta_dict[key])
    return result_list


if __name__=='__main__':
    compile_all()
