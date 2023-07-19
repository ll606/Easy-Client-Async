from typing import Union, Sequence, Optional, Literal
from pywebio.output import Output, popup, close_popup, PopupSize
from pywebio.utils import random_str
from pywebio.pin import pin_wait_change, put_actions
from pywebio.session import run_js


async def confirm(
    title: str,
    content: Union[str, Output, Sequence[Union[str, Output]]] = None,
    *,
    timeout: int = None,
    size: Literal['extra_large', 'large', 'normal', 'samll'] = 'normal',
    center: bool = True,
) -> Optional[bool]:

    if content is None:
        content = []
    if not isinstance(content, list):
        content = [content]
    action_name = random_str(10)

    content.append(put_actions(action_name, buttons=[
        {'label': '确认', 'value': True},
        {'label': '取消', 'value': False, 'color': 'danger'},
    ]).style('margin-top: 1rem; float: left;'))
    popup(title=title, content=content, closable=False, size=PopupSize.LARGE)
    run_js('setModalSize(size)', size=size)
    if center:
        run_js('setModalCentered()')
    result = await pin_wait_change(action_name, timeout=timeout)
    if result:
        result = result['value']
    close_popup()
    return result

class context_confirm:
    
    def __init__(
        self,
        title: str, 
        *,
        timeout: Optional[int] = None,
        size: Literal['extra_large', 'large', 'normal', 'samll'] = 'normal',
        center: bool = True
    ) -> None:
        self.title: str = title
        self.timeout: int = timeout
        self.size: Literal['extra_large', 'large', 'normal', 'samll'] = size
        self.center = center
    
    async def __aenter__(self):
        self.scope = popup(title=self.title, closable=False, size=PopupSize.LARGE)
        self.scope.__enter__()
        run_js('setModalSize(size)', size=self.size)
        if self.center:
            run_js('setModalCentered()')
        return self 
    
    async def __aexit__(self, *args, **kwargs):
        action_name = random_str(10)
        put_actions(action_name, buttons=[
            {'label': '确认', 'value': True},
            {'label': '取消', 'value': False, 'color': 'danger'},
        ]).style('margin-top: 1rem; float: left;')
        
        self.scope.__exit__(None, None, None)
        result = await pin_wait_change(action_name, timeout=timeout)
        if result:
            self.result = result['value']
        close_popup()
        

# @contextmanager
# def context_confirm(
#     title: str,
#     *,
#     timeout: int = None,
#     size: Literal['extra_large', 'large', 'normal', 'samll'] = 'normal',
#     center: bool = True,
# ) -> Optional[bool]:

#     scope = popup(title=title, closable=False, size=PopupSize.LARGE)
#     scope.__enter__()
#     run_js('setModalSize(size)', size=size)
#     if center:
#         run_js('setModalCentered()')
#     yield
#     action_name = random_str(10)
    
    # put_actions(action_name, buttons=[
    #     {'label': '确认', 'value': True},
    #     {'label': '取消', 'value': False, 'color': 'danger'},
    # ]).style('margin-top: 1rem; float: left;')
    # scope.__exit__(None, None, None)
    # result = pin_wait_change(action_name, timeout=timeout)
    # if result:
    #     result = result['value']
    # close_popup()
    # return result