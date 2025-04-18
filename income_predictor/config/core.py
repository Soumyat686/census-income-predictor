# config/core.py
import os
import yaml
#import income_predictor
from pathlib import Path
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
def get_config_path():
    """Get the configuration file path"""
    # Navigate to the directory containing this file and get the config file
    dir_path = os.path.dirname(os.path.realpath(__file__).replace('config', ''))
    config_path = os.path.join(dir_path, 'config.yml')
   # print (config_path)
    return config_path

def get_config():
    """Load configuration from config.yml"""
    config_path = get_config_path()
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
   #     print ("config",config)
    return config

def get_project_root():
    """Get the project root directory"""
    # Config is in project_root/config, so go up one level
    #print("project_root",os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def get_data_path():
    """Get the data directory path"""
    config = get_config()
    root_dir = get_project_root()
   # print("data_path",os.path.join(root_dir, config['data']['raw_path']))
    return os.path.join(root_dir, config['data']['raw_path'])

def get_models_path():
    """Get the models directory path"""
    config = get_config()
    root_dir = get_project_root()
    #print("models_path",os.path.join(root_dir, config['paths']['models_dir']))
    return os.path.join(root_dir, config['paths']['models_dir'])


if __name__ == "__main__":
    get_config()
    get_models_path()
    get_project_root()
    get_data_path()
