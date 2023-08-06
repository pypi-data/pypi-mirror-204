import webview
import re
import os
from distutils.dir_util import copy_tree
from threading import Thread


from .handle_build import handle_build_copy
from .api import Api

_window = None

build_dir = "./build"
build_html = ""
win_name = ""

base_directory = None
if os.name == 'posix':  # for *nix systems
    base_directory = os.path.join(os.path.expanduser('~'), '.pywebview')
elif os.name == 'nt':  # for Windows
    base_directory = os.path.join(os.environ['APPDATA'], 'pywebview')

exposed_fcs = []
CLOSABLE = True


def expose_functions(*fc):
    for f in fc:
        exposed_fcs.append(f)


def init(src, window_name="Hello World!"):
    global build_html
    global win_name

    win_name = window_name
    client_dir = os.path.dirname(src)
    build_html = build_dir + "/" + os.path.basename(src)
    handle_build_copy(client_dir, build_dir, build_html)


def set_CLOSABLE(_val):
    global CLOSABLE
    CLOSABLE = _val


def get_CLOSABLE():
    return CLOSABLE


HIDE_ON_CLOSE = False


def set_HIDE_ON_CLOSE(_val):
    global HIDE_ON_CLOSE
    HIDE_ON_CLOSE = _val


def get_HIDE_ON_CLOSE():
    return HIDE_ON_CLOSE


def on_closing():
    if HIDE_ON_CLOSE:
        def hide():
            _window.hide()
        t = Thread(target=hide)
        t.daemon = True
        t.start()
        return False
    return CLOSABLE


def toggleHide(_is_hidden=False):
    if _is_hidden:
        _window.show()
    else:
        _window.hide()


def create_window(width=800, height=600,
                  x=None, y=None, resizable=True, fullscreen=False, min_size=(200, 100),
                  hidden=False, frameless=False, easy_drag=True,
                  minimized=False, on_top=False, confirm_close=False, background_color='#FFFFFF',
                  transparent=False, text_select=False, zoomable=False, draggable=False, port=None, debug=True):
    global _window
    _window = webview.create_window(title=win_name, url=build_html, js_api=Api(_window), width=width, height=height,
                                    x=x, y=y, resizable=resizable, fullscreen=fullscreen, min_size=min_size,
                                    hidden=hidden, frameless=frameless, easy_drag=easy_drag,
                                    minimized=minimized, on_top=on_top, confirm_close=confirm_close, background_color=background_color,
                                    transparent=transparent, text_select=text_select, zoomable=zoomable, draggable=draggable)

    for fc in exposed_fcs:
        _window.expose(fc)
    _window.events.closing += on_closing
    webview.start(gui='edgehtml', debug=debug,
                  http_port=port, storage_path=base_directory)
