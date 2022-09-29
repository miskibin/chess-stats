import logging.config
import os
from logging import Logger, getLogger

import yaml


class FailedToLoadLoggingConfigException(Exception):
    pass


def get_logger(
    lvl: int = None,
    config_path: os.path = os.path.join("src", "common", "logging.yaml"),
) -> Logger:
    """Returns a logger object, configured with the logging.yaml file."""
    config_path = os.path.join(os.getcwd(), config_path)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found")
    with open(config_path, "rt", encoding="utf-8") as f:
        config = yaml.safe_load(f.read())
    try:
        logging.config.dictConfig(config)
    except ValueError as exc:
        raise FailedToLoadLoggingConfigException from exc
    logger = getLogger("chess_logger")
    if lvl:
        logger.setLevel(lvl)
    return logger
