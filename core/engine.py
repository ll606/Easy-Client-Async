import os
import importlib
from .view import ViewManager, is_view, ViewBase
from inspect import getmembers
from .exceptions import ViewNotFoundError
from pywebio.output import (
    put_tabs, put_scope, use_scope
)
from pywebio.session import set_env, run_async
from component.put_sidebar import put_sidebar, show_tab
from component.scope_with_class import put_html_scope
from .static_file_loader import StaticFileLoader
from types import ModuleType
from typing import List, Dict
import yaml
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
    
    view_path = 'views/'

    def __new__(cls) -> 'Engine':
        if not hasattr(cls, 'instance'):
            set_env(output_max_width='100%')
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

    def scan_dir(self, path: str) -> None:
        if path not in ViewManager.views:
            ViewManager.views[path] = {}

        for each in os.listdir(path):
            dirpath = os.path.join(path, each)
            if os.path.isdir(dirpath):
                module: ModuleType = self.load_file(os.path.join(path, each, 'view'))
                view: ViewBase = self.get_view_obj(module)
                ViewManager.views[path][each] = view
            
            if not os.path.basename(path) in ViewManager.view_config:
                with open(os.path.join(path, 'config.yaml'), 'r', encoding='utf8') as f:
                    ViewManager.view_config[os.path.basename(path)] = yaml.load(f, yaml.FullLoader)
                    
            if os.path.isfile(os.path.join(path, os.path.basename(path)+'.svg')):
                ViewManager.sidebar_icons[os.path.basename(path)] = os.path.join(path, os.path.basename(path)+'.svg')
            
    
    def scan(self):
        path = self.view_path
        with open(os.path.join(path, 'config.yaml'), 'r', encoding='utf8') as f:
            ViewManager.sidebar_config = yaml.load(f, yaml.FullLoader)
        
        for folder in os.listdir(path):
            folder = os.path.join(path, folder)
            if os.path.isdir(folder):
                self.scan_dir(folder)
        

    async def run(self) -> None:
        put_scope('head')
        put_html_scope('body', cls='container')
        put_scope('foot')
        with use_scope('head'):
            put_scope('head-message')
        
        # 登录界面
        while not await (
            ScopeManager.temporary_form('body', 'login')(
                LoginViewHandler()
            )()):
            continue
        
        with use_scope('body'):
            put_html_scope('row-scope', cls='row')
            with use_scope('row-scope'):
                put_html_scope('sidebar', cls='col')
                put_html_scope('content', cls='col')
                
        
        sidebar_data = []
        folders = [each for each in os.listdir(self.view_path) 
                       if os.path.isdir(os.path.join(self.view_path, each))]
        for folder in folders:
            title = ViewManager.sidebar_config.get(folder, folder)
            icon = ViewManager.sidebar_icons.get(folder)
            sidebar_data.append({'title': title, 'scope': put_scope(folder), 'icon': icon})
        
        with use_scope('sidebar'):
            put_sidebar(sidebar_data, 'content')
        show_tab(folders[0])
        for menu_item, view_data in ViewManager.views.items():
            tabs: List[Dict] = []
            for name in view_data.keys():
                basename = os.path.basename(menu_item)
                tabs.append(
                    {
                        'content': put_scope(name.replace('/', '-')),
                        'title': ViewManager.view_config.get(basename, {name:name})[name]
                    }
                )
            
            with use_scope(os.path.basename(menu_item)):
                put_tabs(tabs)
        
            for name, view in view_data.items():
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
