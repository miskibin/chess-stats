import os
from logging import getLogger
from unittest import mock
from unittest.mock import MagicMock

import pytest

from games_parser.api_communicator import GamesHolder, InvalidResponseFormatException


class TestGamesHolder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = getLogger()
        self.holder = GamesHolder(
            chess_com_usr="Barabasz60", logger=self.logger, games=0, time_class="blitz"
        )

    def test_set_games(self):
        games = self.holder._GamesHolder__set_games(None, 10, "blitz")
        assert len(games) == 0
        with pytest.raises(InvalidResponseFormatException):
            GamesHolder._GamesHolder__set_games(["some game"], -1, "blitz")

    def test_set_chess_com_games(self):
        with pytest.raises(SystemExit):
            self.holder._GamesHolder__set_chess_com_games(
                "not existing username X2345fdgJDed", 10, "blitz"
            )
