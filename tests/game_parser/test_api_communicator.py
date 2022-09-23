from logging import getLogger

import pytest
from chessdotcom.types import ChessDotComError

from games_parser.api_communicator import GamesHolder, InvalidResponseFormatException


class TestGamesHolder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = getLogger()
        self.holder = GamesHolder(logger=self.logger)

    def test_set_games(self):
        games = self.holder._GamesHolder__set_games(None, 10, "blitz")
        assert len(games) == 0
        with pytest.raises(InvalidResponseFormatException):
            self.holder._GamesHolder__set_games(["some game"], -1, "blitz")

    def test_set_chess_com_games(self):
        with pytest.raises(ChessDotComError):
            self.holder._GamesHolder__set_chess_com_games(
                "not existing username X2345fdgJDed", 10, "blitz"
            )
