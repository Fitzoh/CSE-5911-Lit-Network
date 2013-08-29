#!/usr/bin/python
"""Parse hugo_downloads.txt file, save picked object representation.

EXPECTED HEADERS
HGNC ID	Approved Symbol	Approved Name	Status	Previous Symbols	Synonyms	Chromosome	Date Modified	Accession Numbers	Entrez Gene ID	Ensembl Gene ID	RefSeq IDs	UniProt ID

python parse_hugo.py
"""
import cPickle as pickle
from __init__ import *
from hugo_gene_symbols.hugo import Hugo, FNAME, FNAME_PKL

def main():
  print "Loading %s into Hugo object..." % FNAME
  H = Hugo()
  H.from_filename = FNAME
  print "Saving pickled Hugo object to %s..." % FNAME_PKL
  pickle.dump(H, open(FNAME_PKL,"w"), -1)
  # list of all official symbols
  official_fname = FNAME_PKL.rpartition('.')[0]+".official.txt"
  print "Saving index as plain text to %s..." % official_fname
  fp = open(official_fname,"w")
  for s in sorted(H.official.keys()):
    fp.write("%s\n"%s)
  fp.close()
  # unique alias mappings
  uniquemap_fname = FNAME_PKL.rpartition('.')[0]+".uniquemap.tab"
  print "Saving unique alias to official symbol mapping to %s..." % uniquemap_fname
  fp = open(uniquemap_fname,"w")
  for a in sorted(H.unique_alias):
    fp.write("%s\t%s\n"%(a,H.unique_alias[a]))
  fp.close()
  # aliases that map to multiple official symbols
  dupemap_fname = FNAME_PKL.rpartition('.')[0]+".dupemap.tab"
  print "Saving alias to multiple symbol mapping (dupes) to %s..." % dupemap_fname
  fp = open(dupemap_fname,"w")
  for a in sorted(H.dupe_alias):
    fp.write("%s\t%s\n"% (a,"\t".join(sorted(H.dupe_alias[a]))))
  fp.close()
  # symbol to entrez ID
  sym2entrez_fname = FNAME_PKL.rpartition('.')[0]+".sym2entrez.tab"
  print "Saving sym2entrezsymbol mapping to %s..." % sym2entrez_fname
  fp = open(sym2entrez_fname,"w")
  for sym in sorted(H.official):
    entrez = H.official[sym]["Entrez Gene ID"]
    fp.write("%s\t%s\n" % (sym,entrez))
    try:
      int(entrez)
    except:
      print "WARNING: entrez [%s] for sym '%s' is not integer string." % (entrez, sym)
  
    

if __name__ == "__main__":
  main()
