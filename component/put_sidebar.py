from typing import Dict
from pywebio.output import Output, put_widget, put_html, use_scope
from pywebio.session import run_js
from pywebio.io_ctrl import output_register_callback
from typing import Sequence, Union, Callable, Optional
from dominate import tags
from dominate.util import raw

def _sidebar_content_scope_wrapper(scope: Output, scopename: str) -> Output:
    tpl = '''
<div class="tab-pane fade" id="list-%s" role="tabpanel" aria-labelledby="list-%s-list">
    {{#contents}}
        {{& pywebio_output_parse}}
    {{/contents}}
</div>
''' % (scopename, scopename)
    return put_widget(tpl, {'contents': [scope]})

def _sidebar_content_scope_list_wrapper(scopes: Dict[str, Output]) -> Output:
    tpl = '''
<div class="tab-content">
    {{#contents}}
        {{& pywebio_output_parse}}
    {{/contents}}
</div>    
'''
    return put_widget(tpl, {
        'contents': 
            [_sidebar_content_scope_wrapper(scope, scopename) 
             for scopename, scope in scopes.items()]}
    )
    

def put_sidebar(contents: Sequence[Dict[str, Union[Output, Callable]]], content_scope: str) -> Output:
    sidebar = tags.div(cls='list-group text-nowrap sidebar text-center', role='tablist')
    scopes = {}
    for i, data in enumerate(contents):
        scope = data['scope']
        text = data['title']
        callback: Optional[Callable] = data.get('callback')
        scopename = scope.spec['dom_id']
        scope.spec['scope'] = 'pywebio-scope-%s' % content_scope
        scopes[scopename] = scope
        sidebar += tags.a(
            text, 
            cls='list-group-item list-group-item-action',
            id='list-%s-list' % scopename,
            href='#list-%s' % scopename,
            data_toggle='tab',
            aria_controls=text,
            aria_selected='true' if i==0 else 'false',
            role="tab"
        )
        
        if callback is not None and callable(callback):
            callback_id = output_register_callback(callback)
            js = '''
                document.querySelector('#list-%s-list').addEventListener('click', event=>{
                    WebIO.pushData('%s', '%s');
                })
            ''' %(scopename, text, callback_id)
            sidebar += tags.script(raw(js))
    with use_scope(content_scope):
        _sidebar_content_scope_list_wrapper(scopes)
    return put_html(sidebar.render())

def show_tab(scopename: str):
    run_js(
        '''$('#list-pywebio-scope-%s-list').tab('show')''' % scopename
    )