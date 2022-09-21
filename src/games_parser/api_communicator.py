import json
import os
from datetime import datetime
from logging import Logger
from pathlib import Path
from pprint import pprint

import chessdotcom
import pandas as pd

from src.games_parser.game import Game
from src.games_parser.utils import get_field_value, get_pgn


class FailedToGetResponseException(Exception):
    pass


class GamesHolder:
    """Class to hold all the games played on `Chess.com`of a given player player.
    TODO extend to lichess.org

    """

    def __init__(
        self, chess_com_usr: str, logger: Logger, games: int, time_class
    ) -> None:
        """_summary_

        Args:
            chess_com_usr (str): username on chess.com to get games from
            logger (Logger): logger to log to
            games (int): number of lastest games to get
            time_class (_type_): time class of games to get (blitz, rapid, bullet, daily)
        """
        self._logger = logger
        self.chess_com_usr = chess_com_usr
        self.eco = self.__set_eco()
        self.chess_com_games = self.__set_chess_com_games(
            chess_com_usr, games, time_class
        )

    def __set_eco(self) -> list[str]:
        with open(
            os.path.join(Path(__file__).parent, Path("openings.json")), encoding="utf-8"
        ) as f:
            eco = json.load(f)
        return eco

    def __set_chess_com_games(
        self, usr: str, games_num: int, time_class: str
    ) -> list[Game]:
        if not usr:
            self._logger.error("No username provided")
            return []
        response = chessdotcom.get_player_profile(usr)
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
                resp = chessdotcom.get_player_games_by_month(usr, y, m).json["games"]
                self._logger.debug(f"{y}-{m} : {len(resp)}")
                games += self.__set_games(resp, games_num - len(games), time_class)
                if len(games) >= games_num:
                    return games
        return games

    def __set_games(
        self, response: dict, games_num: int, time_class: str
    ) -> list[Game]:
        if not response:
            self._logger.error("No response from chess.com")
            return []
        games = []
        for game in response:

            if game["time_class"] == time_class:
                self._logger.debug(f" {games_num - len(games)} games to go")
                games.append(
                    Game(game["pgn"], self.chess_com_usr, self._logger, self.eco)
                )
            if len(games) >= games_num:
                return games
        return games

    def convert_to_dataframe(self):
        data = [game.asdict() for game in self.chess_com_games]
        df = pd.DataFrame(data)
        df = df.set_index("date")
        return df

    def save_to_csv(self):
        df = self.convert_to_dataframe()
        df.to_csv(f"data/{self.chess_com_usr}.csv")

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

