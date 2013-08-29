from litnetwork import config as cfg
import os.path
import csv
import hugo_gene_symbols
H = hugo_gene_symbols.load()



#todo fix this
import random
def scoreFn(in_score):
    return random.random()


#change line to desired format, return None if invalid line
def transform_line(line):
    kinase = H.find_sym(line[0])
    gene = H.find_sym(line[1])
    score = scoreFn(line[2])
    if kinase and gene:
        return [kinase, gene, score]
    else:
        return None


def process_file(infile=None, outfile=None):
    #find in and out file name if not given
    basename, _ = os.path.splitext(__file__)
    if not infile:
        infile = os.path.join(cfg.unprocessed_data_dir, basename + '.csv')
    if not outfile:
        outfile = os.path.join(cfg.processed_data_dir, basename + '_processed.csv')
    
    #read and process all lines
    with open(infile) as f:
        reader = csv.reader(f, delimiter='\t')
        data = [transform_line(line) for line in reader if transform_line(line)][1:]
    #write all lines
    with open(outfile, 'wb') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerows(data)

if __name__=='__main__':
    process_file()
