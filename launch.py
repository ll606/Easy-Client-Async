from pywebio import start_server, config
from pywebio.session import defer_call
from pywebio.utils import get_free_port
from core.engine import Engine
import webview
from multiprocessing import Process
import os
from functools import partial
import ctypes
import sys


ctypes.windll.shcore.SetProcessDpiAwareness(1)

def webui(port, open_browser:bool=True):
    @config(title='auto-browser-framework-gui', theme=None)
    def web():
        defer_call(partial(os._exit, 0))
        try:
            Engine().run()
        except Exception as e:
            from component.reminder import error_reminder
            error_reminder(e, 'extra_large')
            sys.exit(0)
    start_server(web, port=port, auto_open_webbrowser=open_browser, cdn=False)

def local(port):
    webview.create_window(
        'auto-browser-framework-gui', 
        'http://127.0.0.1:{port}'.format(port=port),
        width=1280, height=720, min_size=(1280, 720),
        confirm_close=True
    )
    webview.start()


def main():

    port: int = get_free_port()
    p1 = Process(target=partial(webui, port, False))
    p2 = Process(target=partial(local, port))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    p1.close()
    p2.close()
    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        from component.reminder import error_reminder
        error_reminder(e, 'extra_large')
        sys.exit(0)