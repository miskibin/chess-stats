from games_parser.chess_com_api_communicator import ChessComApiCommunicator
from games_parser.lichess_api_communicator import LichessApiCommunicator
from games_parser.api_communicator import ApiCommunicator
from logging import Logger


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
        "chess": ChessComApiCommunicator,
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
        if portal not in self.COMMUNICATORS:
            self._logger.error(
                f"Invalid portal: {portal}. Valid portals are: {self.COMMUNICATORS.keys()}"
            )
            raise ValueError(f"Invalid portal: {portal}")
        communicator_class = self.COMMUNICATORS[portal]
        return communicator_class(self._logger, depth)


from miskibin import get_logger

factory = CommunicatorFactory(get_logger(lvl=10))
communicator = factory.get_communicator("chess.com")
games = communicator.get_games("pro100wdupecvb", 10, "blitz")
for game in games:
    print(game)
