from .models import Report
from .models import ChessGame as Game
from django.db import models
from django.db.models import F
from logging import Logger
from miskibin.utils import get_logger
from time import time


class QueriesMaker:
    """
    This class is used to create queries for the report.
    It is as most generic as possible.
    To add a new query, add a method that starts with "get_" and returns the data.
    """

    def __init__(self, report: Report, logger: Logger) -> None:
        self.report = report
        self.logger = logger
        self.white = 0
        self.black = 0
        self.get_methods = [
            method
            for method in dir(self)
            if callable(getattr(self, method)) and method.startswith("get")
        ]

    def asdict(self) -> dict:
        """
        This method is used to get the data from the queries.
        it will return a dict with the name of the method (- get_) as key and the data as value.
        eg.
        get_username -> username: "miskibin"
        """
        data = {}
        for method in self.get_methods:
            start = time()
            data[str(method.split("get_")[1])] = getattr(self, method)()
            self.logger.debug(f"Query {method:40} {time() - start:.3f}s")
        self.logger.debug(f"{data.keys()}")
        return data

    def get_all_reports(self) -> list:
        return list(
            Report.objects.all()
            .values("chess_com_username", "lichess_username")
            .distinct()
        )

    def get_analyzed_games(self) -> int:
        return Game.objects.filter(report=self.report).count()

    def get_games_num(self) -> int:
        return self.report.games_num

    def get_chess_com_username(self) -> str:
        return self.report.chess_com_username

    def __get_win_ratio(self, color) -> int:
        win, lost, draws = 0, 0, 0
        win = Game.objects.filter(
            report=self.report, player_color=color, result=F("player_color")
        ).count()
        lost = Game.objects.filter(
            report=self.report, player_color=color, result=1 - F("player_color")
        ).count()
        draws = Game.objects.filter(
            report=self.report, player_color=color, result=0.5
        ).count()
        return [win, draws, lost]

    def get_win_ratio_per_color(self) -> list:
        white = self.__get_win_ratio(0)
        black = self.__get_win_ratio(1)
        return white + black

    def get_player_elo_over_time(self) -> list:
        games = Game.objects.filter(report=self.report).order_by("-date")
        data = []
        day = games[0].date.day
        for game in games:
            if game.date.day != day:
                day = game.date.day
                data.append({"x": game.date, "y": game.player_elo})
        return data

    def get_win_ratio_per_opening_and_color(
        self, max_oppenings=5, short=True
    ) -> tuple[dict]:
        default_field_name = "opening"
        field_name = "opening"
        if short:
            field_name = "short_opening"
        openings_per_color = [{}, {}]
        for color in [0, 1]:
            openings = (
                Game.objects.filter(report=self.report, player_color=color)
                .values(field_name)
                .annotate(count=models.Count(field_name))
            )
            openings = sorted(openings, key=lambda x: x["count"], reverse=True)
            openings = openings[:max_oppenings]
            # change field_name to default_field_name
            for opening in openings:
                opening[default_field_name] = opening.pop(field_name)
            openings_per_color[color] = self.__get_win_ratio_per_opening(
                openings, default_field_name, color
            )
        return openings_per_color

    def __get_win_ratio_per_opening(self, openings, field_name, color):
        for opening in openings:
            opening["win"] = Game.objects.filter(
                report=self.report,
                player_color=color,
                opening__contains=opening[field_name],
                result=F("player_color"),
            ).count()
            opening["lost"] = Game.objects.filter(
                report=self.report,
                player_color=color,
                opening__contains=opening[field_name],
                result=1 - F("player_color"),
            ).count()
            opening["draws"] = Game.objects.filter(
                player_color=color,
                report=self.report,
                opening__contains=opening[field_name],
                result=0.5,
            ).count()
        return openings

    def get_mistakes_per_phase(self):
        data = {}
        games = Game.objects.filter(report=self.report)
        for phase, phase_name in enumerate(["Opening", "Middle", "End"]):
            blunders, mistakes, inacuracies = 0, 0, 0
            games_count = games.count()
            if games_count == 0:
                continue
            for game in games:
                inacuracies += game.mistakes[phase][0]
                mistakes += game.mistakes[phase][1]
                blunders += game.mistakes[phase][2]
                if phase == 1 and game.phases[0] == game.phases[1]:
                    games_count -= 1
                elif phase == 2 and game.phases[1] == game.phases[2]:
                    games_count -= 1
            self.logger.debug(
                f"games_count: {games_count}, blunders: {blunders}, mistakes: {mistakes}, inacuracies: {inacuracies}, phase: {phase}"
            )
            data[phase_name] = [
                inacuracies / games_count,
                mistakes / games_count,
                blunders / games_count,
            ]
        return data
