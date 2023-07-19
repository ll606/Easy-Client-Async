from typing import Sequence, Optional, Callable, Literal
from pywebio.output import Output, popup, close_popup, toast
from pywebio.pin import put_actions, pin_wait_change, pin
from pywebio.utils import random_str
from core.tool.validate_input import validate_input, all_inputs_valid
from pywebio.session import run_js
import asyncio

async def popup_input(
        pins: Sequence[Output],
        title='Please fill out the form below',
        validates: Optional[Sequence[dict[str, str]]] = None,
        size: Literal['extra_large', 'large', 'normal', 'samll'] = 'normal',
        callback: Optional[Callable] = None
) -> Optional[dict]:
    
    if validates is None:
        validates = []
    
    if isinstance(validates, dict):
        validates = [validates]
    
    if not isinstance(pins, list):
        pins = [pins]

    pin_names = [
        p.spec['input']['name']
        for p in pins
        if 'input' in p.spec and 'name' in p.spec['input']
    ]
    action_name = 'action_' + random_str(10)
    pins.append(put_actions(action_name, buttons=[
        {'label': '确定', 'value': True},
        {'label': '取消', 'value': False, 'color': 'danger'},
    ]))
    popup(title=title, content=pins, closable=False)
    run_js('setModalCentered()')
    run_js('setModalSize(size)', size=size)
    
    if callback is not None:
        callback()
    
    for data in validates:
        validate_input(data['name'], data['pattern'], data['success'], data['fail'])

    names = [each['name'] for each in validates]
    
    while True:
        change_info = await pin_wait_change(action_name)
        if await all_inputs_valid(names):
            break
        else:
            if not change_info['value']:
                close_popup()
                return None 
            toast('请确保表单填写正确！', color='rgba(200, 0, 0, 0.7)')
    result = None
    if change_info['name'] == action_name and change_info['value']:
        tasks = [pin[name] for name in pin_names]
        result = {name: res for name, res in 
                  zip(pin_names, await asyncio.gather(*tasks))}
    close_popup()
    return result

class context_popup:
    
    def __init__(self,
        title='Please fill out the form below',
        size: Literal['extra_large', 'large', 'normal', 'samll'] = 'normal',
    ) -> None:
        self.title = title
        self.size = size
    
    
    def __aenter__(self):
        self.popup_scope = popup(title=self.title, closable=False)
        self.popup_scope.__enter__()
        run_js('setModalCentered()')
        run_js('setModalSize(size)', size=self.size)
        return self 
    
    def __aexit__(self, *args, **kwargs):
        action_name = 'action_' + random_str(10)
        put_actions(action_name, buttons=[
            {'label': '确定', 'value': True},
            {'label': '取消', 'value': False, 'color': 'danger'},
        ])
        close_popup()