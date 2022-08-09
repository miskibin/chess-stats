from Log import get_logger
from datetime import datetime
from utils import get_field_value, get_pgn
from logging import Logger
from enum import Enum
from Player import Player, Color
import numpy as np


class InvalidResultException(Exception):
    pass


class Result(Enum):
    White = 0
    Black = 1
    Draw = .5


class Game:
    """ Class representing a game."""

    def __init__(self, pgn: str, username: str, logger: Logger = get_logger()) -> None:
        self._logger = logger
        self._pgn = get_pgn(pgn)
        self.time_control = self.__set_time_control()
        color = bool(self.__set_color(username))
        self.player = Player(pgn, Color(color).value,
                             self.time_control, logger)
        self.opponent = Player(pgn, not Color(
            color).value, self.time_control, logger)
        self.result = self.__set_result()
        self.date = self.__set_date()

    def __set_color(self, username) -> Color:
        if username in get_field_value(self._pgn.headers, "White"):
            return Color.White
        return Color.Black

    def __set_result(self) -> Result:
        RESULT = {
            "1-0": 1,
            "0-1": 0,
            "1/2-1/2": 0.5
        }
        result = get_field_value(self._pgn.headers, "Result")
        try:
            return Result(RESULT[result])
        except KeyError as exc:
            self._logger.error("Invalid result: " + result)
            raise InvalidResultException("Invalid result: " + result) from exc

    def __set_date(self):
        date = get_field_value(self._pgn.headers, "UTCDate")
        time = get_field_value(self._pgn.headers, "UTCTime")
        date_time = datetime.strptime(date + ' ' + time, '%Y.%m.%d %H:%M:%S')
        return date_time

    def __set_time_control(self):
        temp = get_field_value(self._pgn.headers, "TimeControl")
        if '/' in temp: # daily time control
            temp = temp.split('/')[1]
        if '+' not in temp:
            temp = temp + '+0'
        if len(temp.split('+')) != 2:
            self._logger.error("Invalid time control: " + temp)
            raise Exception("Invalid time control: " + temp)
        return temp

    def __str__(self) -> str:
        tree = str(type(self).__name__) + '\n'
        for key, val in self.__dict__.items():
            if key[0] != '_':
                tree += key + ': ' + str(val) + '\n'
        return tree
    
    @staticmethod
    def get_time_class(t_c:str)->str:
        time = int(t_c.split('+')[0])
        if time < 3:
            return 'bullet'
        if time < 10:
            return 'blitz'
        if time < 30:
            return 'rapid'
        return 'classical'
    def asdict(self) -> dict:
        temp = self.time_control.split('+')
        t_c = str(int(temp[0])//60) + '+' + str(temp[1])
        return {
            'player_elo': self.player.elo,
            'opponent_elo': self.opponent.elo,
            'result': self.result.value,
            'date': self.date,
            'time_control': t_c,
            'player_color': self.player.color.value,
            'mean_player_time_per_move': round(np.mean(self.player.time_per_move), 2),
            'mean_opponent_time_per_move': round(np.mean(self.opponent.time_per_move), 2),
            'moves': max(len(self.player.time_per_move), len(self.opponent.time_per_move)),
            'time_class': self.get_time_class(t_c),
            'player_result':abs(self.result.value - self.player.color.value)
        }
