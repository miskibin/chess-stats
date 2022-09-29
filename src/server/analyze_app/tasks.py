from games_parser.api_communicator import GamesHolder
from src.common.utils import get_logger

from . import models


def get_games(
    username: str, games: int, time_class: str, depth: int, *args, **kwargs
) -> None:
    logger = get_logger()
    raport = models.Raport(
        username=username, time_class=time_class, games_num=games, engine_depth=depth
    )
    raport.save()
    g = GamesHolder(logger, depth=depth)
    try:
        for game in g.get_games(username, games, time_class):
            obj = models.ChessGame(**game.asdict(), raport=raport)
            raport.analyzed_games += 1
            raport.save()
            obj.save()
            logger.debug(f"Analyzed {raport.analyzed_games} games")
    except Exception as exc:
        logger.error(exc)
        raport.analyzed_games = -1
        raport.save()
        raise exc
    logger.debug(f"Analyzed {raport.analyzed_games} games")


def convert_data(games: list[models.ChessGame]) -> list[dict]:
    dict_games = []
    for game in games:
        dict_game: dict = game.__dict__
        dict_game.pop("_state")
    dict_games.append(dict_game)
    return dict_games
