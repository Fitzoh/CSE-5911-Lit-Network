from litnetwork.cleaners import Human_Kinase_Interactom as hki
from litnetwork.cleaners import comKSI as ksi

def clean_all():
    '''Cleans all source files. New source files must be added manually.'''
    hki.process_file()
    ksi.process_file()
