import yaml

from robot.api import Error
from yaml.loader import SafeLoader

class FileYaml():
    ### Load data file yaml  ###
    def read_yaml_file(self, filename:str):
        absolute_path = f'{filename}.yaml'
        try:
            with open(absolute_path) as f:
                return yaml.load(f, Loader=SafeLoader)
        except Exception as e:
            raise Error(e)