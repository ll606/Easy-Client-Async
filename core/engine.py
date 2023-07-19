import os
import importlib
from .view import ViewManager, is_view, ViewBase
from inspect import getmembers
from .exceptions import ViewNotFoundError
from pywebio.output import (
    put_tabs, put_scope, use_scope
)
from pywebio.session import set_env, run_async
from .static_file_loader import StaticFileLoader
from types import ModuleType
from typing import List
from .scopeManager import ScopeManager
from .login_view import LoginViewHandler


class Engine:
    """
    引擎类管理Web应用程序中视图的执行和扫描。

    属性:
        instance: Engine类的实例。单例模式。

    方法:
        load_file: 根据给定的模块路径加载Python模块。
        get_view_obj: 从加载的模块中检索视图对象。
        scan: 扫描'views/'目录以查找视图模块，并将其添加到ViewManager中。
        run: 执行Web应用程序的视图。

    """

    def __new__(cls) -> 'Engine':
        if not hasattr(cls, 'instance'):
            set_env(output_max_width='80%')
            cls.instance = object.__new__(cls)
            cls.instance.scan()
            StaticFileLoader.scan()
        return cls.instance

    @staticmethod
    def load_file(module_path: str) -> ModuleType:
        module_path = module_path.replace('\\', '.').replace('/', '.')
        module = importlib.import_module(module_path)
        return module

    @staticmethod
    def get_view_obj(module) -> ViewBase:
        for _, obj in getmembers(module):
            if is_view(obj):
                return obj
        else:
            raise ViewNotFoundError(
                'Unable to find view in the module of %s.' % module.__name__
            )

    def scan(self) -> None:
        path = 'views/'

        for each in os.listdir(path):
            dirpath = os.path.join(path, each)
            if os.path.isdir(dirpath):
                module: ModuleType = self.load_file(os.path.join(path, each, 'view'))
                view: ViewBase = self.get_view_obj(module)
                ViewManager.views[each] = view

        ViewManager.close()

    async def run(self) -> None:
        # 登录界面
        while not await (
            ScopeManager.temporary_form('body', 'login')(
                LoginViewHandler()
            )()):
            continue
        
        tabs: List[dict] = []
        for name in ViewManager.views.keys():
            tabs.append(
                {
                    'content': put_scope(name), 
                    'title': ViewManager.get_view_config().get(name, name)
                }
            )

        put_scope('head') 
        put_scope('body') 
        put_scope('foot')
        
        with use_scope('head'):
            put_scope('head-message')

        with use_scope('body', clear=True):
            put_tabs(tabs)
        
        for name, view in ViewManager.views.items():
            view: ViewBase
            try:
                run_async(use_scope(name, clear=True)(view().render)())
            except Exception as e:
                from component.confirm import confirm
                from pywebio.output import put_markdown
                from traceback import format_exception
                error = ''.join(format_exception(e))
                await confirm(
                    '⚠ Warning: %s' % e.__class__.__name__,
                    put_markdown(
                        '### This error will not crash the programme. '
                        'However, it will lead to part of the programme'
                        ' unusable. \n`Error Details:`\n<pre style="background:'
                        'transparent"> %s </pre>' % error, 
                    ), size='extra_large'
                )
