import bleach


def sanitize_input(s: str):
    if not s:
        return s
    return bleach.clean(s)
