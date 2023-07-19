from core.view import ViewBase
from pywebio.output import put_scope, put_markdown

class View(ViewBase):
    
    # def __init__(self) -> None:
    #     put_scope('start-head')
    #     put_scope('start-body')
    #     put_scope('start-foot')
    
    async def render(self):
        put_markdown(
            '# Hello, World'
        )