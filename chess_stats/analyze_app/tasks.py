from logging import Logger

from easy_logs import get_logger
import chess_insight
from chess_insight.api_communicator import ApiCommunicator
from . import models


def get_games(
    report: models.Report, logger: Logger = get_logger(lvl=10), *args, **kwargs
) -> None:
    games_num_per_host = report.games_num // sum(
        1 if host else 0
        for host in [report.chess_com_username, report.lichess_username]
    )
    hosts = {
        "chess.com": report.chess_com_username,
        "lichess.org": report.lichess_username,
    }

    for host, username in hosts.items():
        if username:
            communicator = chess_insight.get_communicator(
                host,
                report.engine_depth,
                "./stockfish.exe",
            )
            # valid_name = communicator.get_valid_username(username) # TODO uncomment
            valid_name = username
            if not valid_name:
                report.fail_reason = f"Connection issues or user {username} is invalid"
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
        for game in communicator.games_generator(
            username, games_num, report.time_class
        ):
            opponent = models.SingleGamePlayer(**game.opponent.asdict())
            player = models.SingleGamePlayer(**game.player.asdict())
            game_dict = game.asdict()  # remove player and opponent from game_dict
            del game_dict["player"]
            del game_dict["opponent"]
            obj = models.ChessGame(
                **game_dict, report=report, player=player, opponent=opponent
            )
            report.analyzed_games += 1
            report.save()
            obj.save()
            logger.debug(f"Analyzed {report.analyzed_games} games")
    except Exception as exc:
        logger.error(exc)
        report.analyzed_games = -1
        report.save()
        raise exc
