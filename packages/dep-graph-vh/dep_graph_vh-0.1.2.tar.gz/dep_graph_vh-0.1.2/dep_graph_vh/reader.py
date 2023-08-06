"""
This module contains functions to read dependencies from the input JSON file
(provided or system-specific default one)

:raises FileNotFoundError: if the input file does not exist
"""
import json
import os
import sys
from typing import List, Dict

WINDOWS_DEFAULT_PATH = 'C:\\tmp\\deps.json'
UNIX_DEFAULT_PATH = '/tmp/deps.json'


def is_platform_windows() -> bool:
    """
    Check if the current platform is windows

    :return: true, if platform is windows, false for all other cases
    """
    return sys.platform == "win32"


def get_default_file_path() -> str:
    """
    Get the default system-specific path for the dependencies json file

    :return: string representing default path
    """
    if is_platform_windows():
        return WINDOWS_DEFAULT_PATH

    return UNIX_DEFAULT_PATH


def read_dependencies(file_path) -> Dict[str, List[str]]:
    """
    Read the dependencies from the json file

    :param file_path: absolute location of the dependencies file
    :raises FileNotFoundError: if the file does not exist
    :return: parsed dict of dependencies
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Input file {file_path} does not exist")

    with open(file_path, encoding='utf8') as json_file:
        return json.load(json_file)
