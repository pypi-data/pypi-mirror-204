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
