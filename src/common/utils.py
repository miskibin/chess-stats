import logging.config
import os
from logging import Logger, getLogger

import yaml
from marshmallow.exceptions import ValidationError
from yamldataclassconfig.config import YamlDataClassConfig as YDMC

from src.common.logging_config_utils import PackagePathFilter


class FailedToLoadLoggingConfigException(Exception):
    pass


def get_logger(lvl: int = None, config_path: str = "src/common/logging.yaml") -> Logger:
    """Returns a logger object, configured with the logging.yaml file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found")
    with open(config_path, "rt", encoding="utf-8") as f:
        config = yaml.safe_load(f.read())
    try:
        logging.config.dictConfig(config)
    except ValueError as exc:
        raise FailedToLoadLoggingConfigException from exc
    logger = getLogger("chess_logger")
    logger.addFilter(PackagePathFilter())
    if lvl:
        logger.setLevel(lvl)
    return logger

