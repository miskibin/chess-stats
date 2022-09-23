import json
import os
from datetime import datetime
from logging import Logger
from pathlib import Path

import chessdotcom
import pandas as pd
from chessdotcom.types import ChessDotComError
from games_parser.game import Game


class InvalidResponseFormatException(Exception):
    pass


class GamesHolder:
    """Class to hold all the games played on `Chess.com`of a given player player.
    TODO extend to lichess.org

    """

    def __init__(self, logger: Logger) -> None:
        """_summary_

        Args:
            logger (Logger): logger to log to

        """
        self._logger = logger
        self.eco = self.__set_eco()
        self.chess_com_games = None

    def get_games(self, chess_com_usr: str, games: int, time_class: str):
        """
        Args:
            chess_com_usr (str): username on chess.com to get games from
            games (int): number of lastest games to get
            time_class (_type_): time class of games to get (blitz, rapid, bullet, daily)
        returns:
            list[Game]: list of `Game` objects
        """

        self.__set_chess_com_games(chess_com_usr, games, time_class)
        return self.chess_com_games

    def __set_eco(self) -> list[str]:
        with open(
            os.path.join(Path(__file__).parent, Path("openings.json")), encoding="utf-8"
        ) as f:
            eco = json.load(f)
        return eco

    def __set_chess_com_games(self, usr: str, games_num: int, time_class: str) -> None:
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
        games = []
        for y in range(datetime.now().year, year - 1, -1):
            if y == datetime.now().year:
                m = datetime.now().month
            else:
                m = 12
            while m > 0:
                if y == int(datetime.now().year) and m >= int(datetime.now().month):
                    break
                resp = chessdotcom.get_player_games_by_month(usr, y, m).json
                self._logger.debug(f"{y}-{m} : {len(resp)}")
                games += self.__set_games(
                    resp["games"], games_num - len(games), time_class, usr
                )
                if len(games) >= games_num:
                    self.chess_com_games = games
                    break
        self.chess_com_games = games

    def __set_games(
        self, json_with_games: list, games_num: int, time_class: str, usr: str
    ) -> list[Game]:
        if not json_with_games:
            self._logger.error("No response from chess.com")
            return []
        if not isinstance(json_with_games, list) or not isinstance(
            json_with_games[0], dict
        ):
            self._logger.error("Invalid response format")
            raise InvalidResponseFormatException
        games = []
        for game in json_with_games:
            if game["time_class"] == time_class:
                self._logger.debug(f" {games_num - len(games)} games to go")
                games.append(Game(game["pgn"], usr, self._logger, self.eco))
            if len(games) >= games_num:
                return games
        return games

    def convert_to_dataframe(self):
        data = [game.asdict() for game in self.chess_com_games]
        df = pd.DataFrame(data)
        df = df.set_index("date")
        return df

    def __str__(self) -> str:
        return str(
            f"games played on chess.com: {len(self.chess_com_games)}\
                   \nexample game:\n{str(self.chess_com_games[0])}"
        )

    def __repr__(self) -> str:
        tree = ""
        for game in self.chess_com_games:
            tree += str(game) + "\n"
        return tree


from src.common.utils import get_logger
import logging

logger = get_logger(logging.DEBUG)
g = GamesHolder(logger)

g.get_games("Barabasz60", 1, "blitz")
from pprint import pprint

pprint(g)
