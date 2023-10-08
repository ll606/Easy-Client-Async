from abc import ABCMeta, abstractmethod
from typing import Any, Dict
from types import MappingProxyType
from .exceptions import InitiationLimitError
from yaml import load, FullLoader

class ViewBase(metaclass=ABCMeta):
    """
    视图基类，定义了视图渲染的抽象方法。

    方法:
        render: 渲染视图的抽象方法。

    """
    
    @abstractmethod
    def render(self, *args, **kwargs) -> None:
        raise NotImplementedError
    
def is_view(obj: Any) -> bool:
    """
    检查对象是否为视图类。
    """
    if not isinstance(obj, type):
        return False
    
    if not issubclass(obj, ViewBase):
        return False 
    
    if obj.__name__ == 'ViewBase':
        return False
    
    return True


class ViewManager:
    """
    视图管理器类，用于管理和配置视图。

    属性:
        views: 视图字典，保存视图名称和对应的视图对象。

    方法:
        close: 关闭视图管理器，将views属性设为只读字典。
        get_view_config: 获取视图配置字典。

    """
    
    views: Dict[str, Dict[str, ViewBase]] = {}
    view_config: Dict[str, Dict[str, str]] = {}
    sidebar_config: Dict[str, str] = {}
    sidebar_icons: Dict[str, str] = {}
    
    def __new__(cls) -> 'ViewManager':
        raise InitiationLimitError(
            'The class of %s cannot be initiated!' % cls.__name__
        )
    
    @classmethod
    def close(cls) -> None:
        cls.views = MappingProxyType(cls.views)
        cls.view_config = MappingProxyType(cls.view_config)
        cls.sidebar_config = MappingProxyType(cls.sidebar_config)
    