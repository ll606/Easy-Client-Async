from abc import ABCMeta, abstractmethod
from core.tool.validate_input import all_inputs_valid


class AbstractFormHandler(metaclass=ABCMeta):
    
    @abstractmethod
    def __call__(self, value: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def result(self) -> dict[str, str]:
        raise NotImplementedError
    
    @abstractmethod
    def all_inputs_valid(self) -> bool:
        raise NotImplementedError
    
class BaseFormHandler(AbstractFormHandler):
    
    def __init__(self) -> None:
        pass
    
    def result(self) -> dict[str, str]:
        pass
    
    def all_inputs_valid(self) -> bool:
        return all_inputs_valid([each['name'] for each in self.input_names])
    
    def __call__(self, value: str) -> None:
        pass