from typing import Any

class Logger(object):
    current_indent = 0
    # items beyond this level of indent will __NOT__ be printed
    max_indent = 5

def increase_indent():
    Logger.current_indent += 1

def decrease_indent():
    Logger.current_indent -= 1

def log(obj: Any, indent: int = None):
    if indent is None: indent = Logger.current_indent
    if indent > Logger.max_indent: return
    print("  " * indent, obj, sep="")