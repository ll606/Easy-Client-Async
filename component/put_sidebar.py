from typing import Dict, List
from pywebio.output import Output, put_widget, put_html, use_scope, put_row, put_scope
from pywebio.session import run_js
from pywebio.utils import random_str
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


def _render_icon(contents: List):
    for i, data in enumerate(contents):
        icon = data.get('icon')
        scope = data['scope']
        scopename = scope.spec['dom_id']
        style = 'margin-top:20px; cursor: pointer;'
        if i == 0:
            style += 'transform: translateY(50%);'
        else:
            style += 'transform: translateY(calc(50% + 20px));'
        if icon is not None:
            with open(icon, 'r', encoding='utf8') as f:
                svg = f.read()
            svg = '<svg fill="currentColor" ' + svg.lstrip('<svg')
            put_html(
            '''
<div data-toggle="tab" 
    class="icon text-nowrap" 
    style="%s"
    onclick="showTab(this, '%s')"
    role="tab"
    aria-controls="%s"
    aria-selected="false"
>%s</div>''' % (style, scopename, data['title'], svg)).send()
        else:
            put_html('<div class="text-nowrap" style="%s"></div>' % style).send()
    

def put_sidebar(contents: Sequence[Dict[str, Union[Output, Callable]]], content_scope: str) -> Output:
    
    sidebar_id = random_str()
    sidebar = tags.div(cls='list-group text-nowrap sidebar text-center', role='tablist', id=sidebar_id)
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
            role="tab",
            onclick="changeIconColor('%s')" % scopename
        )
        
        if callback is not None and callable(callback):
            callback_id = output_register_callback(callback)
            callback_js = '''
                document.querySelector('#list-%s-list').addEventListener('click', event=>{
                    WebIO.pushData('%s', '%s');
                })
            ''' %(scopename, text, callback_id)
            sidebar += tags.script(raw(callback_js))
    
    show_tab_js = '''    
function showTab(element, scopename) {
    $('#list-'+scopename+'-list').tab('show');
    element.setAttribute('aria-selected', true);
    element.style.color = '#0366d6';
    for(let icon of document.querySelectorAll('.icon[role="tab"]')){
        if(icon !== element){
            icon.setAttribute('aria-selected', false);
            icon.style.color = '#212529';
        }
    }
}

function changeIconColor(scopename) {
    const target = document.querySelector('.icon[onclick*="'+scopename+'"]');
    target.style.color = '#0366d6';
    target.setAttribute('aria-selected', true);
    for(let icon of document.querySelectorAll('.icon[role="tab"]')){
        if(icon !== target){
            icon.setAttribute('aria-selected', false);
            icon.style.color = '#212529';
        }
    }
}
'''

    sidebar += tags.script(raw(show_tab_js))
    with use_scope(content_scope):
        _sidebar_content_scope_list_wrapper(scopes)
    
    icon_scope = random_str()
    put_row([put_scope(icon_scope), put_html(sidebar.render())], size=r'10% 90%').send()
    with use_scope(icon_scope):
        _render_icon(contents)
    

def show_tab(scopename: str):
    run_js(
        '''$('#list-pywebio-scope-%s-list').tab('show')''' % scopename
    )