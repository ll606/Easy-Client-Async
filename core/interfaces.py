from tornado.web import RequestHandler
from typing import Any
from .config import global_config
import importlib
import os
import inspect
from .logger import Logger

class InterfaceRegisteredTwiceError(Exception):
    pass

class UnregisteredInterfaceError:
    pass

class BaseInterface(RequestHandler):

    @classmethod
    def is_interface(cls, target: Any):
        if not isinstance(target, type):
            return False
        
        if not issubclass(target, cls):
            return False
        
        if target is cls:
            return False
        
        return True
    
class InterfaceRegister:
    
    def __init__(self, path: str) -> None:
        self.path = path
        
    def __call__(self, cls: type) -> type:
        if not BaseInterface.is_interface(cls):
            raise TypeError(
                'Only Interface class can be registerred! However, '
                'got %s!' % cls.__name__
            )
        
        if hasattr(cls, '__interface_path__'):
            raise InterfaceRegisteredTwiceError
        
        cls.__interface_path__ = self.path
        return cls
    
class InterfaceLoader:
    
    interface_path = global_config['interface_path']
    interfaces: dict[str, BaseInterface]
    
    @classmethod
    def load(cls):
        if hasattr(cls, 'interfaces'):
            return cls.interfaces
        
        cls.interfaces = {}
        
        for root, _, files in os.walk(cls.interface_path):
            if '__pycache__' in root:
                continue
            
            for file in files:
                if not file.endswith('.py') and not file.endswith('.pyd'):
                    continue
                
                filepath = os.path.join(root, file)
                filepath = filepath.replace('\\', '.').replace('/', '.')
                module = importlib.import_module(filepath)
                for _, obj in inspect.getmembers(module):
                    if not BaseInterface.is_interface(obj):
                        continue
                    
                    if not hasattr(obj, '__interface_path__'):
                        raise UnregisteredInterfaceError(
                            (
                                '%s is an interface, however, it'
                                ' has not been registered'
                            ) % obj.__name__
                        )
                        
                    cls.interfaces[obj.__interface_path__] = obj
                    obj.logger = Logger(
                        name=obj.__name__,
                        extra={
                            'executor': obj.__name__,
                            'task': 'Http Interface'
                        }
                    )
            