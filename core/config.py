import yaml
from types import MappingProxyType


with open('settings/global_config.yaml', 'r', encoding='utf8') as f:
    global_config = yaml.load(f, yaml.FullLoader)
    
global_config = MappingProxyType(global_config)
__all__ = ['global_config']