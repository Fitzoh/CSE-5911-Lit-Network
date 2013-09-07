import csv

def write_file(data, outfile):
    '''Writes cleaned output files in a standardized format.'''
    with open(outfile, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['#kinase', 'gene', 'confidence'])
        writer.writerows(data)
