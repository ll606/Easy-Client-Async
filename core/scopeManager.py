from pywebio.output import get_scope, remove, use_scope, toast, put_scope
from pywebio.session import run_js, eval_js
from pywebio.utils import random_str
from pywebio.pin import put_actions, pin_wait_change
from typing import Optional, Any
from .exceptions import ScopeNotFoundError
from functools import wraps
from component.absctract_form_handler import AbstractFormHandler
from component.card import Card
import asyncio


class ScopeManager:
    """
    作用域管理器类，用于管理和操作作用域。

    方法:
        hide_scope: 隐藏指定作用域。
        show_scope: 显示指定作用域。
        remove_scope: 移除指定作用域。
        get_all_scopes: 获取所有作用域。
        get_subscopes: 获取指定作用域的子作用域。
        get_parent_scope: 获取指定作用域的父作用域。
        get_all_parent_scopes: 获取指定作用域的所有父作用域。
        page_switch: 页面切换装饰器，用于在页面切换时隐藏和显示指定作用域。
        temporary_scope: 临时作用域装饰器，用于在函数执行期间创建临时作用域。
        temporary_form: 临时表单装饰器，用于在表单处理器执行期间创建临时作用域并显示表单。
    """
    
    @classmethod
    def hide_scope(cls, scope: Optional[str]=None, ms: int=200):
        if scope is None:
            scope = get_scope()
        
        run_js(
            'hideElement(selector, period)', 
            selector='#pywebio-scope-%s' % scope,
            period=ms 
        )
    
    @classmethod
    def show_scope(cls, scope: Optional[str]=None, ms: int=200):
        if scope is None:
            scope = get_scope()
        
        run_js(
            'showElement(selector, period)',
            selector='#pywebio-scope-%s' % scope, 
            period=ms
        )
        
    @classmethod
    def hide_element(cls, selector: Optional[str]=None, ms=200):
        run_js(
            'hideElement(selector, period)', 
            selector=selector,
            period=ms 
        )
        
    @classmethod
    def show_element(cls, selector: Optional[str]=None, ms=200):
        run_js(
            'showElement(selector, period)',
            selector=selector,
            period=ms
        )
    
    @classmethod
    def remove_scope(cls, scope: Optional[str]=None):
        remove(scope)
    
    @classmethod
    def get_all_scopes(cls):
        return eval_js('getAllScopes()')
    
    @classmethod
    def get_subscopes(cls, scope: Optional[str]=None):
        if scope is None:
            scope = get_scope()
        
        res = eval_js('getSubScope(scope)', scope=scope)
        
        if res is None:
            raise ScopeNotFoundError('cannot find the scope of %s.' % scope)
        return res
    
    @classmethod
    def get_parent_scope_by_scope_name(cls, scope: Optional[str]=None):
        if scope is None:
            scope = get_scope()
        res = eval_js('getParentScopeByScope(scope)', scope=scope)
        if res is None:
            raise ScopeNotFoundError('cannot find the scope of %s.' % scope)
        return res
    
    @classmethod
    def get_parent_scope_by_name(cls, name: str):
        res = eval_js('getParentScopeByName(name)', name=name)
        if res is None:
            raise ScopeNotFoundError('cannot find the scope of %s.' % res)
        return res
            
    
    @classmethod
    def get_all_parent_scopes(cls, scope: Optional[str]=None):
        if scope is None:
            scope = get_scope()
        res = eval_js('getAllParentScopes(scope)', scope=scope)
        if res is None:
            raise ScopeNotFoundError('cannot find the scope of %s.' % scope)
        return res
    
    @classmethod
    def page_switch(cls, scope: str) -> Any:
        def decorator(func: callable):
            
            if asyncio.iscoroutinefunction(func):
                @wraps(func)
                async def inner(*args, **kwargs):
                    ScopeManager.hide_scope(scope, 0)
                    res = await func(*args, **kwargs)
                    ScopeManager.show_scope(scope, 300)
                    return res
                    
            else:
                @wraps(func)
                def inner(*args, **kwargs):
                    ScopeManager.hide_scope(scope, 0)
                    res = func(*args, **kwargs)
                    ScopeManager.show_scope(scope, 300)
                    return res
            return inner
        return decorator
    
    @classmethod
    def temporary_scope(cls, scope: Optional[str]=None, style: str='') -> Any:
        if scope is None:
            scope = random_str()
        
        def decorator(func: callable):
            if asyncio.iscoroutinefunction(func):
                @wraps(func)
                async def inner(*args, **kwargs):
                    put_scope(scope).style(style)
                    with use_scope(scope, clear=True):
                        res = await func(*args, **kwargs)
                    remove(scope)
                    return res
            else:
                @wraps(func)
                def inner(*args, **kwargs):
                    put_scope(scope).style(style)
                    with use_scope(scope, clear=True):
                        res = func(*args, **kwargs)
                    remove(scope)
                    return res
            return inner
        return decorator
    
    @classmethod
    def temporary_form(cls, 
        back_to_page: str, 
        temp_scope: Optional[str]=None,
    ):
        """
        临时表单装饰器，用于在表单处理器执行期间创建临时作用域并显示表单。

        参数:
            back_to_page: 返回的页面名称。
            temp_scope: 临时作用域名称，如果未指定，则自动生成一个随机字符串作为作用域名称。

        返回:
            装饰器函数。

        """
        
        if temp_scope is None:
            temp_scope = random_str()
        
        def decorator(handler: AbstractFormHandler):
            
            if hasattr(handler, 'style'):
                if isinstance(handler.style, str):
                    style = handler.style
                elif isinstance(handler.style, dict):
                    style = ';'.join('%s:%s' % (k,v) for k,v in handler.style.items())
            else:
                style = ''
            
            if hasattr(handler, 'title'):
                title = handler.title
            else:
                title = '表单'
            
            
            @wraps(handler)
            @cls.page_switch(back_to_page)
            @cls.temporary_scope(temp_scope, style)
            async def inner(*args, **kwargs):
                
                with Card(title):
                    res = handler(*args, **kwargs)
                    action_name = 'action-%s' % random_str()
                    put_actions(
                        name=action_name,
                        buttons=[
                            {'label': '确定', 'color': 'primary', 'value': True}, 
                            {'label': '取消', 'color': 'danger', 'value': False}
                        ]
                    )
                while True:
                    action_result = await pin_wait_change(action_name)
                    if action_result['value']:
                        _c = handler.all_inputs_valid()
                        if asyncio.iscoroutine(_c):
                            _c = await _c
                        
                        if _c:
                            if asyncio.iscoroutinefunction(handler.result):
                                return await handler.result()
                            else:
                                return handler.result()
                        else:
                            if not hasattr(handler, 'error_reminder'):
                                toast('请确保表单正确！', color='rgba(255,0,0,0.7)')
                            else:
                                if asyncio.iscoroutinefunction(handler.error_reminder):
                                    await handler.error_reminder()
                                else:
                                    handler.error_reminder()
                    else:
                        return res
            return inner
        return decorator