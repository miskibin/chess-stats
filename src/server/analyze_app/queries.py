from logging import Logger
from time import time

from django.db import models
from django.db.models import Count, F
from django.db.models.query import QuerySet
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
        For each games
        This method is used to get the data from the queries.
        it will return a dict with the name of the method (- get_) as key and the data as value.
        eg.
        get_username -> username: "miskibin"
        """
        games_per_hosts: [str, QuerySet[Game]] = {
            host["host"].replace(".", "_"): Game.objects.filter(
                report=self.report, host=host["host"]
            )
            for host in Game.objects.filter(report=self.report)
            .values("host")
            .distinct()
        }
        games_per_hosts["total"] = Game.objects.filter(report=self.report)
        data = {}
        for method in self.get_methods:
            start = time()
            data[str(method.split("get_")[1])] = {
                host_name: getattr(self, method)(games)
                for host_name, games in games_per_hosts.items()
            }
            self.logger.debug(f"Query {method:40} {time() - start:.3f}s")

        self.logger.debug(f"{data.keys()}")
        return data

    def get_Xanalyzed_games(self, games: QuerySet[Game]) -> int:
        return games.filter(report=self.report).count()

    def get_Xgames_num(self, games: QuerySet[Game]) -> int:
        return len(games)

    def get_Xusername(self, games: QuerySet[Game]) -> str:
        if games[0].host == "lichess.org":
            return games[0].report.lichess_username
        if games[0].host == "chess.com":
            return games[0].report.chess_com_username

    def get_win_ratio_per_color(self, games: QuerySet[Game]) -> list:
        white = self.__get_win_ratio(self.white, games)
        black = self.__get_win_ratio(self.black, games)
        data_dict = {"white": white, "black": black}
        return data_dict

    def __get_win_ratio(self, color, games: QuerySet[Game]) -> int:
        win = games.filter(
            report=self.report, player_color=color, result=F("player_color")
        ).count()
        lost = games.filter(
            report=self.report,
            player_color=color,
            result=1 - F("player_color"),
        ).count()
        draws = games.filter(report=self.report, player_color=color, result=0.5).count()
        return [win, draws, lost]

    def get_win_ratio_per_opening_as_white(self, games: QuerySet[Game]) -> dict:
        return self.__get_win_ratio_per_opening_for_color(games, self.white)

    def get_win_ratio_per_opening_as_black(self, games: QuerySet[Game]) -> dict:
        return self.__get_win_ratio_per_opening_for_color(games, self.black)

    def __get_win_ratio_per_opening_for_color(
        self, games: QuerySet[Game], color: int, max_oppenings=5, short=True
    ) -> tuple[dict]:
        default_field_name = "opening"
        field_name = "opening"
        if short:
            field_name = "short_opening"
        openings = (
            games.filter(report=self.report, player_color=color)
            .values(field_name)
            .annotate(count=models.Count(field_name))
        )
        openings = sorted(openings, key=lambda x: x["count"], reverse=True)
        openings = openings[:max_oppenings]
        for opening in openings:
            opening[default_field_name] = opening.pop(field_name)

        for opening in openings:
            for res, (m, a) in (("win", (1, 0)), ("loss", (-1, 1)), ("draw", (0, 0.5))):
                opening[res] = Game.objects.filter(
                    report=self.report,
                    player_color=color,
                    opening__contains=opening[default_field_name],
                    result=m * F("player_color") + a,
                ).count()
        return openings

    # def get_player_elo_over_time(self) -> list:
    #     games = (
    #         Game.objects.filter(report=self.report)
    #         .annotate(dcount=Count("host"))
    #         .order_by("-date")
    #     )
    #     data = []
    #     day = games[0].date.day
    #     for game in games:
    #         if game.date.day != day:
    #             day = game.date.day
    #             data.append({"x": game.date, "y": game.player_elo, "host": game.host})
    #     return data

    def get_mistakes_per_phase(self, games: QuerySet[Game]):
        data = {}
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
