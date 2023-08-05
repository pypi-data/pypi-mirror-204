import webview
import re
import os
from distutils.dir_util import copy_tree

_window = None

build_dir = "./build"
client_dir = ""
client_html = ""
build_html = ""
win_name = ""

base_directory = None
if os.name == 'posix':  # for *nix systems
    base_directory = os.path.join(os.path.expanduser('~'), '.pywebview')
elif os.name == 'nt':  # for Windows
    base_directory = os.path.join(os.environ['APPDATA'], 'pywebview')

exposed_fcs = []
_closable = True


class Api:
    def __init__(self):
        self._window = None

    def getWindowInfo(self):
        return {"x": _window.x, "y": _window.y, "width": _window.width, "height": _window.height}

    def minimizeWindow(self):
        return _window.minimize()

    def unminimizeWindow(self):
        return _window.restore()

    def hideWindow(self):
        return _window.hide()

    def unhideWindow(self):
        return _window.show()

    def toggleFullscreen(self):
        return _window.toggle_fullscreen()

    def moveWindow(self, _x, _y):
        return _window.move(_x, _y)

    def resizeWindow(self, _width, _height):
        return _window.resize(_width, _height)

    def setWindowName(self, _name):
        return _window.set_title(_name)

    def readFile(self, _path):
        with open(_path, 'r') as file:
            return file.read()

    def writeFile(self, _path, content):
        with open(_path, 'w') as file:
            file.write(content)

    def mkdir(self, _path):
        os.mkdir(_path)

    def readdir(self, _path):
        return os.listdir(_path)

    def pathExists(self, _path):
        return os.path.exists(_path)

    def isfile(self, _path):
        return os.path.isfile(_path)

    def isdir(self, _path):
        return os.path.isdir(_path)


def expose_function(fc):
    exposed_fcs.append(fc)


def check_for_modules(js_path):
    script_dir = os.path.dirname(js_path)
    script_str = ""
    with open(js_path, 'r') as f:
        script_content = f.readlines()

    for line in script_content:
        if ("import" in line):
            import_regex = re.compile(r'from \".+\"|from \'.+\'')
            module_path = script_dir + "/" + import_regex.findall(line)[0].replace("from ", "").replace(
                "\"", "").replace("\'", "")
            script_str += check_for_modules(module_path)
        else:
            if (not "export \{" in line):
                script_str += line.replace("export ", "")
    return script_str + "\n"


def handle_build_copy():
    if not os.path.exists(client_dir):
        return
    try:
        copy_tree(client_dir, build_dir)
    except:
        print("from Copy tree")
        return
    script_str = "<script>window.addEventListener('pywebviewready', function () {\nconst PEQUENA = pywebview.api\n"
    new_html = ""
    with open(build_html, 'r') as f:
        html_content = f.readlines()

    for line in html_content:
        if ("<script" in line):
            if ("src=" in line):
                if ("https://" not in line and "http://" not in line):
                    file_regex = re.compile(r'(?:href|src)="([^"]+)"')
                    js_path = os.path.dirname(build_html) + \
                        "/" + file_regex.findall(line)[0]
                    if ("type=\"module\"" in line):
                        script_str += check_for_modules(js_path)
                    else:
                        print("JS_PATH: ", js_path)
                        with open(js_path, 'r', errors='ignore') as f:
                            script_str += f.read() + "\n"
                else:
                    new_html += line
        else:
            new_html += line

    new_html = new_html.replace("</body>", script_str + "})</script>\n</body>")
    with open(build_html, "w") as op:
        op.write(new_html)


def init(client_src, window_name="Hello World!"):
    global client_dir
    global client_html
    global build_html
    global win_name

    win_name = window_name
    client_dir = os.path.dirname(client_src)
    client_html = os.path.basename(client_src)
    build_html = build_dir + "/" + client_html
    handle_build_copy()


def set_closable(_val):
    global _closable
    _closable = _val


def get_closable():
    return _closable


def on_closing():
    return _closable


def create_window(width=800, height=600,
                  x=None, y=None, resizable=True, fullscreen=False, min_size=(200, 100),
                  hidden=False, frameless=False, easy_drag=True,
                  minimized=False, on_top=False, confirm_close=False, background_color='#FFFFFF',
                  transparent=False, text_select=False, zoomable=False, draggable=False, port=None, debug=True):
    global _window
    _window = webview.create_window(title=win_name, url=build_html, js_api=Api(), width=width, height=height,
                                    x=x, y=y, resizable=resizable, fullscreen=fullscreen, min_size=min_size,
                                    hidden=hidden, frameless=frameless, easy_drag=easy_drag,
                                    minimized=minimized, on_top=on_top, confirm_close=confirm_close, background_color=background_color,
                                    transparent=transparent, text_select=text_select, zoomable=zoomable, draggable=draggable)

    for fc in exposed_fcs:
        _window.expose(fc)
    _window.events.closing += on_closing
    webview.start(gui='edgehtml', debug=debug,
                  http_port=port, storage_path=base_directory)
