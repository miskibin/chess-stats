from logging import getLogger

import pytest
from chessdotcom.types import ChessDotComError

from games_parser.api_communicator import GamesHolder


class TestGamesHolder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = getLogger()
        self.holder = GamesHolder(logger=self.logger)

    def test_get_games(self):

        with pytest.raises(ChessDotComError):
            for g in self.holder.get_games(
                "not existing username dsadasa", 10, "blitz"
            ):
                pass
