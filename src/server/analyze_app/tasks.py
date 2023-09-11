from logging import Logger

from easy_logs import get_logger

from games_parser.communicator_factory import CommunicatorFactory
from games_parser.api_communicator import ApiCommunicator
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
    hosts = {
        "chess.com": report.chess_com_username,
        "lichess.org": report.lichess_username,
    }

    for host, username in hosts.items():
        if username:
            communicator = factory.get_communicator(host, report.engine_depth)
            valid_name = communicator.get_valid_username(username)
            if not valid_name:
                report.fail_reason = f"User {username} is not valid"
                report.analyzed_games = -1
                report.save()
                return
            username = valid_name
            report.save()
            logger.info(f"User {username} is valid. Getting games from {host}")
            _update_report(report, logger, username, communicator, games_num_per_host)
    logger.info(f"Analyzed {report.analyzed_games} games. Report is ready 😍 ")


def _update_report(
    report: models.Report,
    logger: Logger,
    username: str,
    communicator: ApiCommunicator,
    games_num: int,
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
