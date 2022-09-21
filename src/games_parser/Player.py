from enum import IntEnum
from logging import Logger

import chess.pgn
from .utils import get_field_value, get_pgn


class InvalidTimeControlException(Exception):
    pass


class Color(IntEnum):
    White = 0
    Black = 1


class Player:
    """Class representing a player."""

    def __init__(
        self, pgn: chess.pgn.Game, color: bool, time_control: str, logger: Logger
    ) -> None:
        self._pgn = get_pgn(pgn)
        self._logger = logger
        self.color = Color(color)
        self.time_per_move = self.__set_time_per_move(color, time_control)
        self.elo = self.__set_rating()

    def __set_rating(self) -> int:
        RATINGS = {0: "WhiteElo", 1: "BlackElo"}
        return int(get_field_value(self._pgn.headers, RATINGS[self.color]))

    def __set_time_per_move(self, color: Color, time_control: list) -> list[float]:
        try:
            time_left, add_time = map(float, time_control.split("+"))
        except ValueError:
            self._logger.error("Invalid time control: " + time_control)
            return [0]
        times = []
        for index, move in enumerate(self._pgn.mainline()):
            if index % 2 == color:
                times.append(round(time_left - move.clock() + add_time, 2))
                time_left = move.clock()
        return times

    def __str__(self) -> str:
        tree = "\n"
        for key, val in self.__dict__.items():
            if key[0] != "_" and key != "time_per_move":
                tree += "\t\t" + key + ": " + str(val) + "\n"
        return tree
