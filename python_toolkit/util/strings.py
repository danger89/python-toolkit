import re
import os
from urllib.parse import urlparse


def duplicate_filename(filename):
    dot_split_parts = filename.split(".")
    mod_index = -1 if len(dot_split_parts) == 1 else -2
    match = re.match(r"^(.*) \(([0-9]+)\)$", dot_split_parts[mod_index])
    if match is not None:
        group1, group2 = match.group(1), match.group(2)
        dot_split_parts[mod_index] = f"{group1} ({int(group2) + 1})"
    else:
        dot_split_parts[mod_index] += " (1)"
    return ".".join(dot_split_parts)


def remove_filename_ext(filename):
    dot_split_parts = filename.split(".")
    if len(dot_split_parts) > 1:
        dot_split_parts.pop(-1)
    return ".".join(dot_split_parts)


def fill_uri_prefix(uri, prefix=None):
    if urlparse(uri).scheme or not prefix:
        return uri
    parse = urlparse(prefix)
    path = (parse.path if parse.path.endswith("/") 
            else os.path.dirname(parse.path) + "/")
    if uri.startswith("/"):
        return f"{parse.scheme}://{parse.netloc}{uri}"
    else:
        return f"{parse.scheme}://{parse.netloc}{path}{uri}"
