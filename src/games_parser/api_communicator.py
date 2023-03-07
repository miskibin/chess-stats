import json
import os
from abc import ABC
from logging import Logger
from pathlib import Path
from typing import Generator

import requests
from stockfish import Stockfish

from games_parser.game import Game


class ApiCommunicator(ABC):
    HOST = None
    API_URL = None

    def __init__(self, logger: Logger, depth: int = 10) -> None:
        """
        Summary:
            Abstract class for API communication. It is used to get games from chess.com, lichess, etc.
            Each subclass should implement get_games method.
        Args:
            logger (Logger): logger to log to
            depth (int, optional): depth of stockfish engine. Defaults to 10.
        """
        self._logger = logger
        self.eco = self.__set_eco()
        try:
            self.stockfish = Stockfish("stockfish.exe", depth=depth)
        except (AttributeError, FileNotFoundError) as err:
            self._logger.error(
                f"Failed to load stockfish engine: Do you have it installed?  {err}"
            )
            self.stockfish = None

    def send_query(
        self, url: str, headers: dict = None, params: dict = None
    ) -> requests.Response:
        """
        Summary:
            Sends query to given url and returns response.
        Args:
            url (str): url to send query to
            headers (dict, optional): headers to send with query. Defaults to None.
            params (dict, optional): params to send with query. Defaults to None.
        Returns:
            response from given url
        """
        try:
            resp = requests.get(url=url, headers=headers, params=params)
            resp.raise_for_status()
        except requests.HTTPError as err:
            self._logger.error(f"Failed to get response from {url}: {err}")
            raise err
        return resp

    def split_pgns(self, text_pgn: str) -> list[str]:
        """
        Summary:
            Splits pgn string into list of pgn strings.
        Args:
            text_pgn (str): pgn string to split
        Returns:
            list of pgn strings
        """
        pgns = text_pgn.split("\n\n\n")
        while pgns and len(pgns[-1]) == 0:
            pgns.pop()
        return pgns

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
                host=self.HOST,
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
