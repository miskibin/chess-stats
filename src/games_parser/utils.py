import io

import chess.pgn


class InvalidVieldNameException(Exception):
    pass


def get_field_value(json_data, field_name):
    """
    Get the value of a field from a json object.
    """
    try:
        value = json_data[field_name]
    except KeyError as exc:
        raise InvalidVieldNameException(field_name) from exc
    return value


def get_pgn(pgn: str) -> chess.pgn.Game:
    """extracts a pgn file."""
    pgn = io.StringIO(pgn)
    game = chess.pgn.read_game(pgn)
    return game
