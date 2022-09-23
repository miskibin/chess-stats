import copy
import logging
import os
from datetime import datetime
from pathlib import Path


class PackagePathFilter(logging.Filter):
    """Logging filter. change: pathname to app_name in log message."""

    def filter(self, record):
        record.pathname = find_part_of_dispacher_name(record.pathname)
        return True  # needs to be returned.


def find_part_of_dispacher_name(path: str) -> str:
    """To make the logs more readable, the function will return name of  part
    from the generated log is coming.
    Assuming each component is in a `src` or` tests` folder.
    """
    orginal_path = copy.copy(path)
    if not path:
        return "Undefined"
    path: Path = Path(path)
    while True:
        if path.parent == path:  # there is no parent folder
            return orginal_path  # we dont know want to stop program with error
        parent_name = path.parent.name
        if parent_name.startswith("src") or parent_name.startswith("tests"):
            return path.name
        path = path.parent


def set_log_file_path(path: str, name: str) -> str:
    """Creates a log file path. Called from the logging.yaml file."""
    if not name:
        name = f'{datetime.now().strftime("%Y-%m-%d_%H")}.log'
    if not os.path.exists(path):
        os.makedirs(path)
    return logging.FileHandler(os.path.join("./logs", name))
