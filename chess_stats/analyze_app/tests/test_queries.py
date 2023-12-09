from django.test import TestCase
from ..models import ChessGame, Report, SingleGamePlayer, Color, Result
from ..queries import QueriesMaker
from django.utils import timezone
from miskibin import get_logger


class QueryTest(TestCase):
    def setUp(self):
        self.report = Report.objects.create(
            chess_com_username="testuser",
            lichess_username="testuser",
            time_class="blitz",
            games_num=2,
            engine_depth=10,
        )
        self.player = SingleGamePlayer.objects.create(
            evaluation={
                "opening": {"inaccuracy": 0, "mistake": 0, "blunder": 0},
                "middle_game": {"inaccuracy": 0, "mistake": 0, "blunder": 0},
                "end_game": {"inaccuracy": 0, "mistake": 0, "blunder": 0},
            },
            elo=1200,
            avg_move_time={"opening": 10, "middle_game": 10, "end_game": 10},
        )
        self.game1 = ChessGame.objects.create(
            report=self.report,
            host="lichess.org",
            player=self.player,
            opponent=self.player,
            date=timezone.now().replace(tzinfo=None),
            opening="C20 King's Pawn Game",
            opening_short="C20",
            phases={"opening": 10, "middle": 20, "end": 30},
            player_color=Color.WHITE,
            result=Result.DRAW,
            end_reason="stalemate",
            time_class="blitz",
            time_control="300+5",
            url="http://example.com/game1",
            username="testuser",
        )
        self.game2 = ChessGame.objects.create(
            report=self.report,
            host="chess.com",
            player=self.player,
            opponent=self.player,
            date=timezone.now().replace(tzinfo=None),
            opening="C20 King's Pawn Game",
            opening_short="C20",
            phases={"opening": 10, "middle": 20, "end": 30},
            player_color=Color.WHITE,
            result=Result.DRAW,
            end_reason="stalemate",
            time_class="blitz",
            time_control="300+5",
            url="http://example.com/game2",
            username="testuser",
        )

        self.query = QueriesMaker(self.report, logger=get_logger(lvl=40))

    def test_FR9_query_data_by_host(self):
        data: dict = self.query.asdict()
        for stat in data.values():
            self.assertIn("lichess_org", stat.keys())
            self.assertIn("chess_com", stat.keys())
            self.assertIn("total", stat.keys())

    def test_FR8_count_number_of_stats(self):
        data: dict = self.query.asdict()
        number_of_add_stats = 4
        self.assertEqual(len(data), 8 + number_of_add_stats)

    def test_FR12_query_data_has_about_section(self):
        data: dict = self.query.asdict()
        for stat in data.values():
            self.assertIn("about", stat.keys())
