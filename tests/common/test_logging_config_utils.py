from src.common.logging_config_utils import find_part_of_dispacher_name, set_log_file_path
import logging
import os
import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("tests/some/path/to/test.py", "some"),
        ("src/some/path/to/file.py", "some"),
        ("invalid/path", "invalid/path"),
        (None, "Undefined"),
    ],
)
def test_find_part_of_dispacher_name(test_input, expected):
    assert find_part_of_dispacher_name(test_input) == expected


def test_set_log_file_path():
    path = "tests/tmp"
    name = None
    if not os.path.exists(path):
        os.makedirs(path)
    file_handler = set_log_file_path(path, name)
    assert isinstance(file_handler, logging.FileHandler)
    name = "testsing"
    file_handler = set_log_file_path(path, name)
    assert name in file_handler.baseFilename
    if os.path.exists(path):
        os.rmdir(path)