#!/usr/bin/python
"""Load Hugo object.

USE:
>>> import hugo_gene_symbols
>>> H = hugo_gene_symbols.load()
>>> print H.find_sym("MySym") # only unique assignments
>>> print H.find_sym("MySym", allow_dupe=True) # may return a set of symbols
>>> print H.official["MySym"] # dict of all known attributes about official symbol
>>> print H.entrez["12345"] # official symbol that corresponds to entrez ID, if any
"""
import cPickle as pickle
import os.path
import hugo

def load(fname=None):
  if fname is None:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), hugo.FNAME_PKL)
  return pickle.load(open(fname))
