#!/usr/bin/python
EXPECTED_HEADER = "HGNC ID	Approved Symbol	Approved Name	Status	Previous Symbols	Synonyms	Chromosome	Date Modified	Accession Numbers	Entrez Gene ID	Ensembl Gene ID	RefSeq IDs	UniProt ID"

COL_NAMES = "HGNC ID", "Approved Symbol", "Approved Name", "Status", "Previous Symbols", "Synonyms", "Chromosome", "Date Modified", "Accession Numbers", "Entrez Gene ID", "Ensembl Gene ID", "RefSeq IDs", "UniProt ID"

FNAME = "hgnc_downloads.txt"
FNAME_PKL = "HUGO_may21.pkl"

class Hugo:
  def __init__(self, fname=FNAME):
    fp = open(fname)
    header = fp.next().strip()
    if header != EXPECTED_HEADER:
      raise Exception, "HUGO Header format not recognized. See EXPECTED_HEADER."

    self.withdrawn = {}
    self.official = {}
    self.unique_alias = {}
    self.dupe_alias = {}
    self.entrez = {}
    self.uniprot = {}
    self.refseq = {}
    self.ensembl = {}
    
    for line in fp:
      row = line.strip('\r\n').split('\t')
      d = dict(zip(COL_NAMES, row))
      if d["Status"] in ("Entry Withdrawn", "Symbol Withdrawn"):
        self.withdrawn[d["Approved Symbol"].split('~')[0]] = d
        continue

      # Save map
      sym = d["Approved Symbol"]
      if "~" in sym: print "WARNING: possibly withdrawn symbol", sym
      altsyms = set(d["Previous Symbols"].split(", ") + d["Synonyms"].split(', '))
      d.update({'altsyms': altsyms})
      assert sym
      self.official[sym] = d

      # Alternate symbol mapping
      for s in altsyms:
        if not s:
          continue
        assert not (s in self.unique_alias and s in self.dupe_alias)
        if s not in self.unique_alias and s not in self.dupe_alias:
          self.unique_alias[s] = sym
        elif s in self.unique_alias:
          alt_sym = self.unique_alias.pop(s, None)
          self.dupe_alias[s] = set([alt_sym, sym])
        else:
          self.dupe_alias[s].add(sym)
          
      self.entrez[d["Entrez Gene ID"]] = sym
      self.uniprot[d["UniProt ID"]] = sym
      for refseq in d["RefSeq IDs"].split(', '):
        self.refseq[refseq] = sym
      self.ensembl[d["Ensembl Gene ID"]] = sym

  def find_sym(self, s, allow_dupe=False):
    """Return official gene symbol given a putative gene symbol.

    if allow_dupe, may return a set of symbols.
    if no unique symbol, return None.
    otherwise, return string of best symbol.
    """
    if s in self.official:
      return s
    if s in self.unique_alias:
      return self.unique_alias[s]
    if s in self.dupe_alias:
      if allow_dupe:
        return self.dupe_alias[s]
      else:
        return None
    return None
