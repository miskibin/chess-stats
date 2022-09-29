import datetime
import json
import os
from logging import getLogger

import pytest

from games_parser.game import Game, InvalidResultException


class TestGame:
    # TODO: add tests for Game class
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = getLogger()
        path = os.path.join(os.path.dirname(__file__), "validation_files/game.json")
        with open(path, "r") as f:
            self.pgn = json.load(f)["pgn"]
        self.game = Game(
            pgn=self.pgn, username="Barabasz60", logger=self.logger, openings=[]
        )

    def test_init(self):
        assert self.game.player.elo == 994
        assert self.game.opponent.elo == 1017
        assert self.game.time_control == "60+0"
        assert self.game.date == datetime.datetime(2018, 12, 2, 15, 20, 55)
        assert self.game.opening == None
        assert self.game.result.value == 0
        assert self.game.phases == (2, 47, 77)
