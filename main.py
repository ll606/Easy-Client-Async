import asyncio
import ctypes
import sys
import threading
import webbrowser
from functools import partial
from multiprocessing import Process
from typing import Literal

import click
import tornado
import webview
from pywebio import config
from pywebio.platform.tornado import wait_host_port, webio_handler
from pywebio.session import defer_call, run_async
from pywebio.utils import STATIC_PATH, get_free_port

from core.engine import Engine
from core.interfaces import InterfaceLoader
from core.logger import Logger

ctypes.windll.shcore.SetProcessDpiAwareness(1)
def webui(port, open_browser:bool=True):
    @config(title='auto-browser-framework-gui', theme=None)
    async def web():
        defer_call(partial(sys.exit, 0))
        try:
            run_async(Engine().run())
        except Exception as e:
            from component.reminder import error_reminder
            await error_reminder(e, 'extra_large')
            sys.exit(0)
    InterfaceLoader.load()
    interfaces = [(k,v) for k,v in InterfaceLoader.interfaces.items()]
    interfaces.append((r'/ui', webio_handler(web, cdn=False)))
    interfaces.append((
        r"/(.*)", tornado.web.StaticFileHandler, 
        {"path": STATIC_PATH, 'default_filename': 'index.html'})
    )
    application = tornado.web.Application(interfaces)
    application.listen(port=port, address='localhost')
    logger = Logger(name='global', extra={'executor': 'server', 'task':'host server'})
    logger.info('服务已启动，端口: %s' % port)
    logger.info('ui界面: http://127.0.0.1:%s/ui' % port)
    async def open_webbrowser_on_server_started(host, port, path):
        url = 'http://%s:%s/%s' % (host, port, path)
        is_open = await wait_host_port(host, port, duration=20)
        if is_open:
            logger.info('Try open %s in web browser' % url)
            threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()
        else:
            logger.error('Open %s in web browser failed.' % url)
        
    if open_browser:
        tornado.ioloop.IOLoop.current().spawn_callback(
            open_webbrowser_on_server_started, '127.0.0.1', port, 'ui'
        )
    tornado.ioloop.IOLoop.current().start()

def local(port):
    webview.create_window(
        'auto-browser-framework-gui', 
        'http://127.0.0.1:{port}/ui'.format(port=port),
        width=1280, height=720, min_size=(1280, 720),
        confirm_close=True
    )
    webview.start()

@click.command
@click.option('--ui', help='启动ui类型')
def main(ui=Literal['web', 'local']):
    if ui not in ['web', 'local']:
        raise ValueError('The arg of ui only accepts "web" or "local". However, got %s.' % ui)
    
    port: int = get_free_port()
    
    if ui == 'web':
        webui(port)
    
    elif ui == 'local':
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
        asyncio.run(error_reminder(e, 'extra_large'))
        sys.exit(0)