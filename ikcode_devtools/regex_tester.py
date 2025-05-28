import re

def apply_regex(pattern, text, flags=0):
    try:
        regex = re.compile(pattern, flags)
        matches = [(m.start(), m.end()) for m in regex.finditer(text)]
        return matches, None
    except re.error as e:
        return [], str(e)
