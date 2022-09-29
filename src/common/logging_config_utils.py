import copy
import logging
import os
from datetime import datetime
from pathlib import Path


def set_log_file_path(path: str, name: str) -> str:
    """Creates a log file path. Called from the logging.yaml file."""
    if not name:
        name = f'{datetime.now().strftime("%Y-%m-%d_%H")}.log'
    if not os.path.exists(path):
        os.makedirs(path)
    return logging.FileHandler(os.path.join("./logs", name))
