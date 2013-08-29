from litnetwork import config as cfg
import os

if not os.path.exists(cfg.processed_data_dir):
    os.makedirs(cfg.processed_data_dir)


