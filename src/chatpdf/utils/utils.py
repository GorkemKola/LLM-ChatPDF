import os
import sys
import logging

logging_str = '[%(asctime)s: %(levelname)s: %(module)s: %(message)s:]'

log_dir = 'logs'
log_filename ='running_logs.log'
log_filepath = os.path.join(
    log_dir, log_filename
)
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger(
    'chatpdf_logger'
)

### read yaml

from box import ConfigBox
from box.exceptions import BoxValueError
import yaml
from ensure import ensure_annotations
from pathlib import Path

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    '''
    Description:
        reads yaml file

    Args:
        path_to_yaml (Path): path like input

    Raises:
        ValueError: if yaml is empty
        e: other exceptions
    
    Returns:
        ConfigBox: ConfigBox type
    '''

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f'yaml file {path_to_yaml} loaded successfully')
            return ConfigBox(content)
        
    except BoxValueError:
        raise ValueError('yaml file is empty')
    
    except Exception as e:
        raise e
    
### create directories

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    '''
    Description:
        create list of directories

    Args:
        path_to_directories (list): list of path of directories:
        verbose (bool): log process
    '''

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f'created directory at: {path}')



import pickle


def save_variable(variable, filename):
    with open(filename, 'wb') as f:
        pickle.dump(variable, f)


import json
from pinecone import Pinecone, ServerlessSpec
import time

def load_variable(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
def load_index(api_key):
    with open('vars/index_info.json', 'r') as f:
        index_info = json.load(f)
    pc = Pinecone(api_key=api_key)
    return pc.Index(index_info['index_name'])