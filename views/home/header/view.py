from core.view import ViewBase
from pywebio.output import put_markdown

class View(ViewBase):
    
    async def render(self):
        put_markdown('# this is header page')