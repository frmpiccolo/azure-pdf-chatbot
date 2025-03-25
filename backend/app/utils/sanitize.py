import re

def sanitize_id(filename: str) -> str:
    # Keep only letters, digits, underscore (_), dash (-), or equal sign (=)
    safe = re.sub(r"[^a-zA-Z0-9_\-=]", "_", filename)
    return safe
