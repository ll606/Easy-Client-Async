from pywebio.input import input
from pywebio.pin import _pin_output
from pywebio.utils import check_dom_name_value
from typing import Callable, Union, Tuple, List
from pywebio.output import OutputPosition

def put_input(name: str = None, label: str = '', type: str = 'text', *, 
          value: Union[str, int] = None, action: Tuple[str, Callable[[Callable], None]] = None,  placeholder: str = None, 
          readonly: bool = None, datalist: List[str] = None, help_text: str = None, scope: str = None,
              position: int = OutputPosition.BOTTOM):
    check_dom_name_value(name, 'pin `name`')
    if action is not None:
        callback = action[1]
        button_name = action[0]
        action = (button_name, lambda x: callback(name))
    single_input_return = input(name=name, label=label, value=value, type=type, placeholder=placeholder,
                                readonly=readonly, datalist=datalist, help_text=help_text, action=action)
    return _pin_output(single_input_return, scope, position)