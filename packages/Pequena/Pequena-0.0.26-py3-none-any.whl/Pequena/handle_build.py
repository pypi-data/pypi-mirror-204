from distutils.dir_util import copy_tree
import os
import re


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


def handle_build_copy(_client_dir, _build_dir, _build_html):
    if not os.path.exists(_client_dir):
        return
    try:
        copy_tree(_client_dir, _build_dir)
    except:
        print("from Copy tree")
        return
    script_str = "<script>window.addEventListener('pywebviewready', function () {\nconst PEQUENA = pywebview.api\n"
    new_html = ""
    with open(_build_html, 'r') as f:
        html_content = f.readlines()

    for line in html_content:
        if ("<script" in line):
            if ("src=" in line):
                if ("https://" not in line and "http://" not in line):
                    file_regex = re.compile(r'(?:href|src)="([^"]+)"')
                    js_path = os.path.dirname(_build_html) + \
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
    with open(_build_html, "w") as op:
        op.write(new_html)
