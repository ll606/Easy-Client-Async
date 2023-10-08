from component.put_sidebar import put_sidebar
from pywebio.output import put_scope, put_text, use_scope, put_row
from pywebio.session import hold, set_env
from pywebio import start_server


def main():
    set_env(output_max_width='100%')
    texts = ['hello', 'world', 'this', 'isa', 'test']
    
    put_row(
        [
            put_scope('sidebar'),
            put_scope('content')
        ], size=r'30% 70%'
    )
    
    with use_scope('sidebar'):
        put_sidebar([
                {'title': each, 'scope': put_scope(each), 'callback': print}
                for each in texts
            ], 'content')
    
    with use_scope('content'):
        for each in texts:
            with use_scope(each):
                put_text(each)
    hold()

            
if __name__ == '__main__':
    start_server(main, auto_open_webbrowser=True)