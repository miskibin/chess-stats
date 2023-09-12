from logging import Logger
from time import time

from django.db import models
from django.db.models import Count, F

from .models import ChessGame as Game
from .models import Report


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
        self.black = 1
        self.get_methods = [
            method
            for method in dir(self)
            if callable(getattr(self, method)) and method.startswith("get")
        ]

    def asdict(self) -> dict:
        """
        `X` - means that given field is not ment to be visualized !!!
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

    def get_Xall_reports(self) -> list:
        reports = list(
            Report.objects.all()
            .values("chess_com_username", "lichess_username")
            .distinct()
        )
        representative_reports = [
            str(
                f"{report['chess_com_username']} {' and '*min(len(report['lichess_username']), 1)}"
                * min(len(report["chess_com_username"]), 1)
                + report["lichess_username"] * min(len(report["lichess_username"]), 1)
            )
            for report in reports
        ]
        return representative_reports

    def get_Xanalyzed_games(self) -> int:
        return Game.objects.filter(report=self.report).count()

    def get_Xgames_num(self) -> int:
        return self.report.games_num

    def get_Xusername(self) -> str:
        data = f"{self.report.chess_com_username}"
        if not self.report.chess_com_username:
            data = f"{self.report.lichess_username}"
        return data

    def __get_win_ratio(self, color, host) -> int:
        win, lost, draws = 0, 0, 0
        win = Game.objects.filter(
            report=self.report, player_color=color, host=host, result=F("player_color")
        ).count()
        lost = Game.objects.filter(
            report=self.report,
            player_color=color,
            host=host,
            result=1 - F("player_color"),
        ).count()
        draws = Game.objects.filter(
            report=self.report, player_color=color, host=host, result=0.5
        ).count()
        return [win, draws, lost]

    def get_win_ratio_per_color(self) -> list:
        host_list = Game.objects.filter(report=self.report).values("host").distinct()
        data_dict = {}
        for host in host_list:
            white = self.__get_win_ratio(0, host["host"])
            black = self.__get_win_ratio(1, host["host"])
            data_dict[host["host"]] = {"white": white, "black": black}
        total_white = [
            sum([data_dict[host]["white"][i] for host in data_dict]) for i in range(3)
        ]
        total_black = [
            sum([data_dict[host]["black"][i] for host in data_dict]) for i in range(3)
        ]
        data_dict["total"] = {"white": total_white, "black": total_black}
        return data_dict

    def get_player_elo_over_time(self) -> list:
        games = (
            Game.objects.filter(report=self.report)
            .annotate(dcount=Count("host"))
            .order_by("-date")
        )
        data = []
        day = games[0].date.day
        for game in games:
            if game.date.day != day:
                day = game.date.day
                data.append({"x": game.date, "y": game.player_elo, "host": game.host})
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
            data[phase_name] = [
                inacuracies / games_count,
                mistakes / games_count,
                blunders / games_count,
            ]
        return data
