import os
from logging import getLogger

import pytest

from games_parser.game import Game, InvalidResultException


class TestGame:
    # TODO: add tests for Game class
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = getLogger()
        pgn = '[Event "F/S Return Match"]\r'
        self.game = Game(pgn=pgn, username="username", logger=self.logger, openings=[])
