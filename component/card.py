from pywebio.session import run_js
from pywebio.output import use_scope, put_scope
from pywebio.utils import random_str
from typing import Optional, Callable
import asyncio

def set_scope_as_card_root(scope: str):
    run_js('setScopeAsCardRoot(scope)', scope=scope)

def set_scope_as_card_header(scope: str, header: str):
    run_js('setScopeAsCardHeader(scope, header)', scope=scope, header=header)
    
def set_scope_as_card_body(scope: str):
    run_js('setScopeAsCardBody(scope)', scope=scope)
    

class Card:
    
    def __init__(self, header: str, scope: Optional[str]=None):
        self.header = header
        self.scope = scope
        self.name = random_str()
    
    def __enter__(self):
        if self.scope is None:
            put_scope('%s-root' % self.name)
        else: 
            with use_scope(self.scope):
                put_scope('%s-root' % self.name)
        
        with use_scope('%s-root' % self.name, clear=True):
            put_scope('%s-header' % self.name)
            put_scope('%s-body' % self.name)
        
        set_scope_as_card_root('%s-root' % self.name)
        set_scope_as_card_header('%s-header' % self.name, self.header)
        set_scope_as_card_body('%s-body' % self.name)
        self.body_scope = use_scope('%s-body' % self.name)
        return self.body_scope.__enter__()

    
    def __exit__(self, *args, **kwargs):
        self.body_scope.__exit__(*args, **kwargs)
    
    def __call__(self, func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            async def decorator(*args, **kwargs):
                with self:
                    res = await func(*args, **kwargs)
                return res
        else:
            def decorator(*args, **kwargs):
                with self:
                    res = func(*args, **kwargs)
                return res
        return decorator