from games_parser.api_communicator import GamesHolder
from src.common.utils import get_logger

from . import models


def get_games(username: str, games: int, time_class: str) -> None:
    raport = models.Raport(
        name=username, username=username, time_class=time_class, games_num=games
    )
    raport.save()
    g = GamesHolder(get_logger())
    for game in g.get_games(username, games, time_class):
        obj = models.ChessGame(**game.asdict(), raport=raport)
        raport.analyzed_games += 1
        raport.save()
        obj.save()
