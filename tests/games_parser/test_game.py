import datetime
import json
import os
from logging import getLogger
from pathlib import Path
import pytest

from games_parser.game import Game, InvalidResultException


class TestGame:
    # TODO: add tests for Game class
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = getLogger()
        games_file = Path(__file__).parent / "validation_files" / "games.txt"
        with open(games_file, "r") as f:
            self.pgn = f.read().split("\n\n\n")[0]
        self.game = Game(
            pgn=self.pgn, username="pro100wdupe", logger=self.logger, openings=[]
        )

    def test_init(self):
        assert self.game.player.elo == 1779
        assert self.game.opponent.elo == 1737
        assert self.game.time_control == "180+0"
        assert self.game.date == datetime.datetime(2022, 5, 26, 16, 51, 4)
        assert self.game.opening == None
        assert self.game.result.value == 0
