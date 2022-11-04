import json
import os
from logging import Logger
from pathlib import Path
from typing import Generator
from stockfish import Stockfish

from games_parser.game import Game
from abc import ABC, abstractmethod


class InvalidUsernameException(Exception):
    pass


class InvalidResponseFormatException(Exception):
    pass


class ApiCommunicator(ABC):
    def __init__(self, logger: Logger, depth: int = 10) -> None:
        """
        Summary:
            Abstract class for API communication. It is used to get games from chess.com, lichess, etc.
            Each subclass should implement get_games method.
        Args:
            logger (Logger): logger to log to
            depth (int, optional): depth of stockfish engine. Defaults to 10.
        """
        self.host = None
        self._logger = logger
        self.eco = self.__set_eco()
        try:
            self.stockfish = Stockfish("stockfish.exe", depth=depth)
        except (AttributeError, FileNotFoundError) as err:
            self._logger.error(
                f"Failed to load stockfish engine: Do you have it installed?  {err}"
            )
            self.stockfish = None

    def games_generator(
        self, username: str, list_of_pgns: int
    ) -> Generator[Game, None, None]:
        """
        Args:
            username (str): username on given portal (lichess, chess.com, etc.) to get games from
            list_of_pgns (int): number of pgn strings to compute
        returns:
            generator of Game objects, each representing a game played on chess.com
        """
        self._logger.info(f"Collected {len(list_of_pgns)} games")
        for game in list_of_pgns:
            game = Game(
                game,
                username,
                self._logger,
                self.eco,
                site=self.host,
                stockfish=self.stockfish,
            )
            yield game

    def __set_eco(self) -> list[str]:
        with open(
            os.path.join(Path(__file__).parent, Path("openings.json")), encoding="utf-8"
        ) as f:
            eco = json.load(f)
        return eco

    def get_games(
        self, username: str, games: int, time_class: str
    ) -> Generator[Game, None, None]:
        """
        Args:
            username (str): username on given portal (lichess, chess.com, etc.) to get games from
            games (int): number of lastest games to get
            time_class (_type_): time class of games to get (blitz, rapid, bullet, daily)
        returns:
            generator of Game objects, each representing a game played on chess.com, licess, etc.
        """
        self._logger.error(f"Method not implemented in {self.__class__.__name__}")
        raise NotImplementedError
