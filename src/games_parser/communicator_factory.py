from logging import Logger

from Levenshtein import distance as lev

from games_parser.api_communicator import ApiCommunicator
from games_parser.chess_com_api_communicator import ChessComApiCommunicator
from games_parser.lichess_api_communicator import LichessApiCommunicator


class CommunicatorFactory:
    def __init__(self, logger: Logger) -> None:
        """
        Summary:
            Factory class for getting ApiCommunicator objects.
        Args:
            logger (Logger): logger to log to
        """
        self._logger = logger

    COMMUNICATORS = {
        "chess.com": ChessComApiCommunicator,
        "lichess.org": LichessApiCommunicator,
        "lichess": LichessApiCommunicator,
        "chessdotcom": ChessComApiCommunicator,
    }

    def get_communicator(self, portal: str, depth: int = 10) -> ApiCommunicator:
        """
        Summary:
            Returns ApiCommunicator object for given portal.
        Args:
            portal (str): portal to get communicator for (chess.com, lichess.org, etc.)
            depth (int, optional): depth of stockfish engine. Defaults to 10.
        Returns:
            ApiCommunicator object for given portal
        """
        # get closest match
        if portal not in self.COMMUNICATORS:
            closest_portal = min(
                self.COMMUNICATORS.keys(), key=lambda x: lev(x, portal)
            )
            self._logger.error(
                f"Portal {portal} not supported. Did you mean {closest_portal}?"
            )
            raise ValueError(f"Invalid portal: {portal}")
        communicator_class = self.COMMUNICATORS[portal]
        return communicator_class(self._logger, depth)


if __name__ == "__main__":
    from miskibin.utils import get_logger

    logger = get_logger(lvl="DEBUG")
    communicator = CommunicatorFactory(logger).get_communicator("lichess.org")
    games = communicator.get_games("pro100wdupe", 3, "blitz")
    for game in games:
        print(game)
    communicator = CommunicatorFactory(logger).get_communicator("chess.com")
    games = communicator.get_games("Barabasz60", 3, "blitz")
    for game in games:
        print(game)
