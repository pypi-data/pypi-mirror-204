import re


def to_snake_case(string: str) -> str:
    # replace all special characters with a space
    string = re.sub(r"[^a-zA-Z0-9]+", " ", string)
    # replace all spaces with _
    string = re.sub(r"\s+", "_", string)
    # make string lowercase
    string = string.lower()
    # remove leading and trailing _
    string = string.strip("_")
    return string

def to_kebab_case(s):
    # Replace all non-letter, non-digit characters with hyphen
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s)
    # Remove leading and trailing hyphens
    s = re.sub(r'^-|-$', '', s)
    # Convert to lower case
    s = s.lower()
    return s

def to_camel_case(s):
    # Replace all non-letter, non-digit characters with space
    s = re.sub(r'[^a-zA-Z0-9]+', ' ', s)
    # Convert to title case
    s = s.title()
    # Remove spaces and join words
    s = ''.join(s.split())
    # Convert first character to lowercase
    s = s[0].lower() + s[1:]
    return s


def str2bool(s):
    if isinstance(s, bool):
        return s
    if isinstance(s, int):
        return bool(s)
    if isinstance(s, str):
        s = s.strip().lower()
        if s in ['yes', 'true', 'on', '1']:
            return True
        elif s in ['no', 'false', 'off', '0', '']:
            return False
        else:
            raise ValueError("String is not a valid boolean representation.")
    if isinstance(s, list):
        return bool(s)

    return False
