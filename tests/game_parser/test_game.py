import pytest
import os
from src.games_parser.game import Game, InvalidResultException
from src.common.utils import get_logger

class TestGame:
    # TODO: add tests for Game class
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = get_logger()
        pgn = "[Event \"F/S Return Match\"]\r"
        self.game = Game(pgn =  pgn, username='username', logger=self.logger, openings=[])
  