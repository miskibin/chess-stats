from logging import Logger

from miskibin.utils import get_logger

from games_parser.communicator_factory import CommunicatorFactory

from . import models


def get_games(
    report: models.Report, logger: Logger = get_logger(lvl=10), *args, **kwargs
) -> None:
    factory = CommunicatorFactory(logger)
    games_num_per_host = report.games_num // sum(
        [
            1 if host else 0
            for host in [report.chess_com_username, report.lichess_username]
        ]
    )
    if report.chess_com_username is not None and report.chess_com_username != "":
        logger.debug("Getting games from chess.com")
        communicator = factory.get_communicator("chess.com", report.engine_depth)
        username = report.chess_com_username
        _update_report(report, logger, username, communicator, games_num_per_host)
    if report.lichess_username is not None and report.lichess_username != "":
        logger.debug("Getting games from lichess")
        communicator = factory.get_communicator("lichess.org", report.engine_depth)
        username = report.lichess_username
        _update_report(report, logger, username, communicator, games_num_per_host)
    logger.info(f"Analyzed {report.analyzed_games} games. Report is ready 😍 ")


def _update_report(
    report: models.Report, logger: Logger, username: str, communicator, games_num: int
) -> None:
    try:
        for game in communicator.get_games(username, games_num, report.time_class):
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


def convert_data(games: list[models.ChessGame]) -> list[dict]:
    dict_games = []
    for game in games:
        dict_game: dict = game.__dict__
        dict_game.pop("_state")
    dict_games.append(dict_game)
    return dict_games
