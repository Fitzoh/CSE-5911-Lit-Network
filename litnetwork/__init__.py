from litnetwork import config as cfg
import os
import litnetwork.cleaners as cln
from litnetwork import compile_processed as cp
from litnetwork import reduce_network as rn
from litnetwork import write_matrices as wm
from litnetwork import convert_to_antibodies as cta

if not os.path.exists(cfg.processed_data_dir):
    os.makedirs(cfg.processed_data_dir)

def gen_all():
    '''Runs entire workflow from uncleaed source files to adjacency matrices.'''
    cln.clean_all()
    print 'cleaning all'
    cp.compile_all()
    print 'compiling network'
    rn.reduce_network()
    print 'reducing network'
    cta.convert_to_antibodies()
    print 'converting to antibodies'
    wm.make_matrices()
    print 'making matrices'
