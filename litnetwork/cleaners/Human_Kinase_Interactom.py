from litnetwork import config as cfg
from litnetwork.cleaners import writer as w
import os.path
import csv
import hugo_gene_symbols
H = hugo_gene_symbols.load()


def scoreFn(category):
    '''Retuns confidence score based on category.'''
    if '1' in category:
        return .1
    if '2' in category:
        return .1
    if '3' in category:
        return .5
    if '4' in category:
        return .6
    return 0


def transform_line(line):
    '''Reformats line, returns None if line is invalid.
    
    Line is invalid if kinase or gene do not correspond to a single
    Hugo id.'''
    kinase = H.find_sym(line[0])
    gene = H.find_sym(line[2])
    score = scoreFn(line[4])
    if kinase and gene:
        return [kinase, gene, score]
    else:
        return None


def process_file(infile=None, outfile=None):
    '''Processes and writes source file to cleaned file.'''
    #find in and out file name if not given
    basename = os.path.split(os.path.splitext(__file__)[0])[1]
    if not infile:
        infile = os.path.join(cfg.unprocessed_data_dir, basename + '.csv')
    if not outfile:
        outfile = os.path.join(cfg.processed_data_dir, basename + '_processed.csv')
    
    #read and process all lines
    with open(infile) as f:
        reader = csv.reader(f, delimiter='\t')
        data = [transform_line(line) for line in reader if transform_line(line)][1:]
    w.write_file(data, outfile)

if __name__=='__main__':
    process_file()
