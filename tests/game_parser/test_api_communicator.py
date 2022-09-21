import pytest
import os
from unittest import mock
from unittest.mock import MagicMock
from src.games_parser.api_communicator import GamesHolder, FailedToGetResponseException
from src.common.utils import get_logger

class TestGamesHolder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = get_logger()
        self.holder = GamesHolder(chess_com_usr='username', logger=self.logger, games=0, time_class='blitz')
        
    def test_set_games(self):
        games = self.holder._GamesHolder__set_games(None,10, 'blitz')
        assert len(games) == 0