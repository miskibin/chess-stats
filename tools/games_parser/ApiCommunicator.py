import chessdotcom
from Game import Game
import json
from logging import Logger
from datetime import datetime
from Log import get_logger
import pandas as pd


class FailedToGetResponseException(Exception):
    pass


class GamesHolder:
    def __init__(self, chess_com_usr=None, lichess_usr=None, logger: Logger = get_logger()) -> None:
        self._logger = logger
        self.chess_com_games = self.__set_chess_com_games(chess_com_usr)
        self.lichess_games = self.__set_lichess_games(lichess_usr)

    def __set_chess_com_games(self, usr) -> list[Game]:
        if not usr:
            return []
        response = chessdotcom.get_player_profile(usr)
        joined = response.json['player']['joined']
        year = datetime.fromtimestamp(joined).year
        games = []
        for y in range(year + 2, datetime.now().year + 1):
            for m in range(1, 13):
                if y == int(datetime.now().year) and m >= int(datetime.now().month):
                    break
                resp = chessdotcom.get_player_games_by_month(
                    usr, y, m).json['games']
                self._logger.debug(f'{y}-{m} - : {len(resp)}')
                games += [Game(game['pgn'], usr, self._logger)
                          for game in resp]
        return games

    def __set_lichess_games(self, usr) -> list[Game]:
        if not usr:
            return []
        return

    def convert_to_dataframe(self):
        data = [game.asdict() for game in self.chess_com_games]
        df = pd.DataFrame(data)
        df = df.set_index('date')
        return df
    def __str__(self) -> str:
        return str(f'games played on chess.com: {len(self.chess_com_games)}\
                   \ngames played on lichess: {len(self.lichess_games)}')

    def __repr__(self) -> str:
        tree = ''
        for game in self.chess_com_games:
            tree += str(game) + '\n'
        return tree


if __name__ == '__main__':
    g = GamesHolder('Barabasz60')
    df = g.convert_to_dataframe()
    df.to_csv('data/games.csv')
