from games_parser.api_communicator import GamesHolder
from miskibin.utils import get_logger
from logging import Logger
from . import models


def get_games(report: models.Report, logger: Logger, *args, **kwargs) -> None:
    g = GamesHolder(logger, depth=report.engine_depth)
    try:
        for game in g.get_games(report.username, report.games_num, report.time_class):
            obj = models.ChessGame(**game.asdict(), report=report)
            report.analyzed_games += 1
            report.save()
            obj.save()
            logger.debug(f"Analyzed {report.analyzed_games} games")
    except Exception as exc:
        logger.error(exc)
        report.analyzed_games = -1
        report.save()
        raise exc
    logger.info(f"Analyzed {report.analyzed_games} games. Report is ready 😍 ")


def convert_data(games: list[models.ChessGame]) -> list[dict]:
    dict_games = []
    for game in games:
        dict_game: dict = game.__dict__
        dict_game.pop("_state")
    dict_games.append(dict_game)
    return dict_games
