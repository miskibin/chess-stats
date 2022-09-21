import pytest
from src.games_parser.utils import get_field_value, get_pgn, InvalidVieldNameException

def test_get_field_value():
    json_data = {"field": "value"}
    assert get_field_value(json_data, "field") == "value"
    with pytest.raises(InvalidVieldNameException) as e:
        get_field_value(json_data, "invalid_field")
    assert e
def test_get_pgn():
    pgn = "[Event \"F/S Return Match\"]\r"
    parsed_pgn = get_pgn(pgn)
    assert parsed_pgn.headers["Event"] == "F/S Return Match"