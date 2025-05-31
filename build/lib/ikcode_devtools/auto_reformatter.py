# auto_reformatter.py

import inspect
import ast
import black

_reformatted_registry = {}

def reFormat(func):
    try:
        source = inspect.getsource(func)
        _reformatted_registry[func.__name__] = source
    except Exception as e:
        print(f"[reFormat] Could not get source for {func.__name__}: {e}")
    return func

def get_decorated_functions():
    return _reformatted_registry.copy()

def reformat_code(code: str) -> str:
    try:
        parsed = ast.parse(code)
        formatted = black.format_str(code, mode=black.FileMode())
        return formatted
    except Exception as e:
        return f"# Error formatting code:\n# {e}"
