"""
Module to parse an os-release config file.
"""

import re
import os
from typing import Dict, List, Optional, Tuple

from .errors import OSRIError


def load(path: str) -> Dict[str, Optional[str]]:
    """
    Load an os-relase config file from a given path.
    """
    data: Dict[str, Optional[str]] = {}

    for line in read_lines(path):
        key, value = parse_line(line)
        if key:
            data[key] = value

    return data


def read_lines(path: str) -> List[str]:
    """
    Open and return an os-release file lines in a list.
    """
    if not os.path.exists(path):
        raise OSRIError(f'path not found: {path}')

    with open(path, 'r') as f:
        lines = f.readlines()

    return [l.replace('\n', '') for l in lines]


def parse_line(line: str) -> Tuple[str, Optional[str]]:
    """
    Parse an os-release line, returning the field name and value
    in a tuple.

    Return tuple with empty strigs `('', '')` if the regex
    fails to match its pattern against the line string.
    """
    p = '^([A-Z_]+)=\"?([a-zA-Z0-9\s\(\)\:\;\-\/\.\,]+)?\"?$'
    s = re.search(p, line)
    if s:
        name = s.group(1).lower()
        value = s.group(2)
        if value is not None:
            value = value.replace('\n', '')

        return (name, value)

    return ('', '')
