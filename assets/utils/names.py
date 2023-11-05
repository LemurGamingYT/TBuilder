from contextlib import suppress


def display_name(name: str) -> str:
    new = []
    for char in name.title():
        with suppress(IndexError):
            if char == '_':
                new.append(' ')
            else:
                new.append(char)
    
    return ''.join(new)

def code_name(name: str) -> str:
    return name.replace(' ', '_').lower()
