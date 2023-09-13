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


def is_chess_960(pgn: chess.pgn.Game) -> bool:
    pgn = get_pgn(pgn)
    return get_field_value(pgn.headers, "Variant") == "Chess960"


def get_time_class(pgn: chess.pgn.Game) -> str:
    pgn = get_pgn(pgn)
    temp = get_field_value(pgn.headers, "TimeControl")
    if "/" in temp:  # daily time control
        temp = temp.split("/")[1]
    if "+" not in temp:
        temp = temp + "+0"
    if len(temp.split("+")) != 2:
        raise Exception("Invalid time control: " + temp)
    time = int(temp.split("+")[0])
    if time < 3 * 60:
        return "bullet"
    if time < 10 * 60:
        return "blitz"
    if time < 30 * 60:
        return "rapid"
    return "classical"
