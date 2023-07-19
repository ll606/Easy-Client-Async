from .confirm import confirm
from traceback import format_exception
from pywebio.output import put_markdown, put_scrollable, Output, put_text
from typing import Literal, Union, List 


async def base_reminder(
    title: str, 
    content: Union[Output, List[Output], str, Exception],
    size: Literal['extra_large', 'large', 'normal', 'samll'] = 'normal',
    format_error: bool = True,
    scrollable: bool = True,
    icon: Literal['error', 'success', 'warning', 'info', 'save', None] = None 
):
    if isinstance(content, Exception) and format_error:
        content = ''.join(format_exception(content))
        
    if isinstance(content, str):
        content = put_text(content)
    
    if scrollable:
        content = put_scrollable(content)
    
    if icon is not None:
        iconmap = {
            'error': '❌',
            'warning': '⚠', 
            'success': '✅',
            'save': '🗃️',
            'info': 'ℹ️'
        }
        
        title = '%s %s' % (iconmap.get(icon), title)
    
    return await confirm(
        title=title, 
        content=content,
        size=size
    )
    
    
async def error_reminder(
    e: Exception, 
    size: Literal['extra_large', 'large', 'normal', 'samll'] = 'extra_large',
):
    return await base_reminder(
        title='%s: %s' % (e.__class__.__name__, str(e)),
        content=e,
        size=size,
        icon='error'
    )
    
async def warning_reminder(
    title: str, 
    content: Union[Output, List[Output], str, Exception],
    size: Literal['extra_large', 'large', 'normal', 'samll'] = 'normal',
):
    return await base_reminder(
        title, 
        content=content,
        size=size,
        icon='warning'
    )
    
async def info_reminder(
    title: str,
    content: Union[Output, List[Output], str, Exception],
    size: Literal['extra_large', 'large', 'normal', 'samll'] = 'normal',
):
    return await base_reminder(title, content, size, icon='info')