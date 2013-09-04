from litnetwork import config as cfg
import os
import litnetwork.cleaners as cln
from litnetwork import compile_processed as cp
from litnetwork import reduce_network as rn
from litnetwork import write_matrices as wm

if not os.path.exists(cfg.processed_data_dir):
    os.makedirs(cfg.processed_data_dir)

def gen_all():
    cln.clean_all()
    cp.compile_all()
    rn.reduce_network()
    wm.make_matrices()
