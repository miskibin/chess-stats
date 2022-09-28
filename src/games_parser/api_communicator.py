import json
import os
from datetime import datetime
from logging import Logger
from pathlib import Path

import chessdotcom
import pandas as pd
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
                f"Failed to load stockfish engine: Do you have it installed? and named `stockfish.exe`? {err}"
            )
            self.stockfish = None
        self.chess_com_games = []

    def get_games(self, chess_com_usr: str, games: int, time_class: str) -> list[Game]:
        """
        Args:
            chess_com_usr (str): username on chess.com to get games from
            games (int): number of lastest games to get
            time_class (_type_): time class of games to get (blitz, rapid, bullet, daily)
        returns:
            list[Game]: list of `Game` objects
        """
        list_of_games = self.__set_chess_com_games(chess_com_usr, games, time_class)
        for game in list_of_games:
            game = Game(
                game["pgn"], chess_com_usr, self._logger, self.eco, self.stockfish
            )
            self._logger.debug(f"{games - len(self.chess_com_games)} games left")
            self.chess_com_games.append(game)
            yield game

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
                m = int(datetime.now().month)
            else:
                m = 12
            while m > 0:
                if int(y) == int(datetime.now().year) and m > int(datetime.now().month):
                    break
                resp = chessdotcom.get_player_games_by_month(usr, y, m).json
                if not isinstance(resp["games"], list) or not isinstance(
                    resp["games"][0], dict
                ):
                    self._logger.error(f"Invalid response format {resp}")
                    raise InvalidResponseFormatException(resp)
                self._logger.debug(
                    f"In {y}-{m} : {len(resp['games'])} games was played"
                )
                for g in resp["games"]:
                    if len(games) >= games_num:
                        return games
                    if g["time_class"] == time_class:
                        games.append(g)
                m -= 1
        return games

    def convert_to_dataframe(self) -> pd.DataFrame:
        if not self.chess_com_games:
            self._logger.error(
                "No games to convert to dataframe. Did you called get_games function?"
            )
            return pd.DataFrame()
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
