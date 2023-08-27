from typing import Any

global default_indent
default_indent: int = 0
# items beyond this level of indent will __NOT__ be printed
global max_indent
max_indent: int = 1

def increase_indent():
    default_indent += 1

def decrease_indent():
    default_indent -= 1

def log(obj: Any, indent: int = None):
    if indent is None: indent = default_indent
    if indent > max_indent: return
    print("  " * indent, obj, sep="")