from src.common.utils import get_logger, FailedToLoadLoggingConfigException
import pytest
import os


def test_get_logger():
    with pytest.raises(FileNotFoundError) as e:
        get_logger(config_path="invalid_path")
    assert e

    path = os.path.join(os.path.dirname(__file__), r"validation_files/invalid_logging_config.yaml")
    with pytest.raises(FailedToLoadLoggingConfigException) as e:
        get_logger(config_path=path)
    assert e
    debug_logger = get_logger(lvl=10)
    assert debug_logger.level == 10

