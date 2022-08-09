import logging
import os
import sys
from datetime import datetime


def get_logger(name=None, path='./logs', to_file=True, level = 1) -> logging.Logger:
    """
    Args:
        name: Name of file where logs will be saved. Defaults to <current_date>_<hour>
        path: Path to dir where logs will be saved. Defaults to './logs'.
        save_to_file: If False will print messages only to console. Defaults to True.
    """
    if not name:
        name = f'{datetime.now().strftime("%Y-%m-%d_%H")}.log'
    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)-8s :: %(filename)-20s :: %(message)s', '%m-%d-%Y %H:%M:%S')
    logging.basicConfig() # reset previous config
    logger = logging.getLogger(name)
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.setLevel(level)
    if to_file:
        if not os.path.exists(path):
            os.makedirs(path)
        file_handler = logging.FileHandler(os.path.join(path, name))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    return logger
