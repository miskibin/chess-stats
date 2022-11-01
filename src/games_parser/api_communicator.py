import json
import os
from datetime import datetime
from logging import Logger
from pathlib import Path

import chessdotcom
from chessdotcom.types import ChessDotComError
from stockfish import Stockfish

from games_parser.game import Game


class InvalidResponseFormatException(Exception):
    pass


class GamesHolder:
    """Class to hold all the games played on `Chess.com`of a given player player.
    TODO extend to lichess.org

    """

    def __init__(self, logger: Logger, depth: int = 10) -> None:
        """_summary_

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

    def get_games(self, chess_com_usr: str, games: int, time_class: str) -> list[Game]:
        """
        Args:
            chess_com_usr (str): username on chess.com to get games from
            games (int): number of lastest games to get
            time_class (_type_): time class of games to get (blitz, rapid, bullet, daily)
        returns:
            list[Game]: list of `Game` objects
        """
        list_of_games = self.__get_chess_com_games(chess_com_usr, games, time_class)
        self._logger.info(f"Collected {len(list_of_games)} games from chess.com")
        for game in list_of_games:
            game = Game(
                game["pgn"], chess_com_usr, self._logger, self.eco, self.stockfish
            )
            yield game

    def __set_eco(self) -> list[str]:
        with open(
            os.path.join(Path(__file__).parent, Path("openings.json")), encoding="utf-8"
        ) as f:
            eco = json.load(f)
        return eco

    def __get_joined_year(self, usr: str) -> int:
        if not usr:
            self._logger.error("No username provided")
            return []
        try:
            response = chessdotcom.get_player_profile(usr)
        except ChessDotComError as err:
            self._logger.error(f"Failed to get response from chess.com: {err.text}")
            raise err
        joined = response.json["player"]["joined"]
        year = datetime.fromtimestamp(joined).year
        return year

    def __get_chess_com_response(self, usr: str, y: int, m: int) -> list:
        try:
            resp = chessdotcom.get_player_games_by_month(usr, y, m).json
            games = resp["games"]
        except (ChessDotComError, KeyError) as err:
            self._logger.error(f"Failed to get response from chess.com: {err.text}")
            raise err
        self._logger.debug(f"In {y}-{m} : {len(games)} games was played")
        return games

    def __get_chess_com_games(self, usr: str, games_num: int, time_class: str) -> None:
        joined_year = self.__get_joined_year(usr)
        games = []
        for y in range(datetime.now().year, joined_year - 1, -1):
            if y == datetime.now().year:
                m = int(datetime.now().month)
            else:
                m = 12
            while m > 0:
                games_json = self.__get_chess_com_response(usr, y, m)

                for g in games_json:
                    if len(games) >= games_num:
                        return games
                    if g["time_class"] == time_class:
                        games.append(g)
                m -= 1
        return games
