import os
import yaml
from yamlinclude import YamlIncludeConstructor

YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir='/opt/elastalert')

def read_yaml(path):
    with open(path) as f:
        yamlContent = os.path.expandvars(f.read())
        return yaml.load(yamlContent, Loader=yaml.FullLoader)
