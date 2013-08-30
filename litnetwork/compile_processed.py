from litnetwork import config as cfg
from collections import defaultdict
import operator
import os
import csv


def compile_all(source_dir=None, dest_file=None):
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
    meta_cols = max(map(len, rows)) - 3
    headers = ['#source', 'target', 'score'] + ['meta' + str(i) for i in range(meta_cols)]
    with open(dest_file, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(headers)
        writer.writerows(rows)


def parse_file(source_file, score_dict, meta_dict):
    with open(source_file) as f:
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            if '#' not in line[0]:
                key = (line[0], line[1])
                score_dict[key].append(float(line[2]))
                meta_dict[key].append(os.path.basename(source_file))


def process_rows(score_dict, meta_dict):
    result_list = []
    for key in score_dict:
        #1-(1-n1)*(1-n2)*(1-n3)...
        score = 1 - reduce(operator.mul, map(lambda x: 1-x, score_dict[key]))
        result_list.append(list(key) + [score] + meta_dict[key])
    return result_list


if __name__=='__main__':
    compile_all()
