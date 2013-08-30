import csv

def write_file(data, outfile):
    with open(outfile, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['#kinase', 'gene', 'confidence'])
        writer.writerows(data)
