import chessdotcom
from src.games_parser.Game import Game
import json
from logging import Logger
from datetime import datetime
import pandas as pd
from pathlib import Path
import os


class FailedToGetResponseException(Exception):
    pass


class GamesHolder:
    def __init__(self, chess_com_usr: str, logger: Logger, games: int, time_class) -> None:
        self._logger = logger
        self.chess_com_usr = chess_com_usr
        self.eco = self.__set_eco()
        self.chess_com_games = self.__set_chess_com_games(
            chess_com_usr, games, time_class)

    def __set_eco(self) -> list[str]:
        with open(os.path.join(Path(__file__).parent, Path('openings.json')), encoding='utf-8') as f:
            eco = json.load(f)
        return eco

    def __set_chess_com_games(self, usr, games_num, time_class) -> list[Game]:
        if not usr:
            return []
        response = chessdotcom.get_player_profile(usr)
        joined = response.json['player']['joined']
        year = datetime.fromtimestamp(joined).year
        games = []
        for y in range(datetime.now().year, year-1, -1):
            if y == datetime.now().year:
                m = datetime.now().month
            else:
                m = 12
            while m > 0:
                if y == int(datetime.now().year) and m >= int(datetime.now().month):
                    break
                resp = chessdotcom.get_player_games_by_month(
                    usr, y, m).json['games']
                self._logger.debug(f'{y}-{m} - : {len(resp)}')
                games += [Game(game['pgn'], usr, self._logger, self.eco)
                          for game in resp if game['time_class'] == time_class]
                m -= 1
                if len(games) >= games_num:
                    return games
        return games

    def convert_to_dataframe(self):
        data = [game.asdict() for game in self.chess_com_games]
        df = pd.DataFrame(data)
        df = df.set_index('date')
        return df

    def save_to_csv(self):
        df = self.convert_to_dataframe()
        df.to_csv(f'data/{self.chess_com_usr}.csv')

    def __str__(self) -> str:
        return str(f'games played on chess.com: {len(self.chess_com_games)}\
                   \nexample game:\n{str(self.chess_com_games[0])}')

    def __repr__(self) -> str:
        tree = ''
        for game in self.chess_com_games:
            tree += str(game) + '\n'
        return tree


if __name__ == '__main__':
    from src.common.utils import get_logger
    g = GamesHolder('Barabasz60', get_logger(), 100, 'rapid')
    print(g)
    #g.save_to_csv()
