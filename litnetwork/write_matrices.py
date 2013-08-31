import litnetwork.config as cfg
import csv

def make_matrices(source_file=None, target_hugo_file=None, length_matrix_file=None, score_matrix_file=None):
    if not source_file:
        source_file = cfg.reduced_data_file
    if not target_hugo_file:
        target_hugo_file = cfg.target_hugo_file
    if not length_matrix_file:
        length_matrix_file = cfg.length_matrix_file
    if not score_matrix_file:
        score_matrix_file = cfg.score_matrix_file
    with open(target_hugo_file) as f:
        targets = set([line.strip() for line in f])
    permuations = [(first,second) for first in targets for second in targets]
    with open(source_file) as f:
        reader = csv.reader(f, delimiter='\t')
        data = [line for line in reader if '#' not in line[0]]
    score_dict = {(line[0],line[1]):line[2] for line in data}
    length_dict = {(line[0], line[1]):line[3] for line in data}
    write_matrix(score_matrix_file, score_dict, targets, 0)
    write_matrix(length_matrix_file, length_dict, targets, -1)

def write_matrix(dest_file, attr_dict, targets, default):
    with open(dest_file, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['']+list(targets))
        for row in targets:
            data = [row]
            for col in targets:
                data.append(attr_dict.get((row,col),default))
            writer.writerow(data)

if __name__=='__main__':
    make_matrices()
