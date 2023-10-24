from logging import Logger
from time import time

from datetime import datetime
from django.db.models import Count, F, Q
from django.db.models.query import QuerySet
from .models import ChessGame as Game
from .models import Report, Color, Result


class QueriesMaker:
    """
    This class is used to create queries for the report.
    It is as most generic as possible.
    To add a new query, add a method that starts with "get_" and returns the data.
    """

    def __init__(self, report: Report, logger: Logger) -> None:
        self.report = report
        self.logger = logger
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
            data[str(method.split("get_")[1])]["about"] = getattr(self, method).__doc__
            self.logger.debug(f"Query {method:40} {time() - start:.3f}s")

        self.logger.debug(f"{data.keys()}")

        return data

    def get_Xanalyzed_games(self, games: QuerySet[Game]) -> int:
        return games.filter(report=self.report).count()

    def get_Xprofessional(self, games: QuerySet[Game]) -> int:
        return self.report.professional

    def get_Xgames_num(self, games: QuerySet[Game]) -> int:
        return len(games)

    def get_win_per_opponent_rating(self, games: QuerySet[Game]) -> dict:
        """
        Win ratio against lower rated players, similarly rated players, and higher rated players.
        """

        def win_ratio(queryset):
            wins = queryset.filter(result=F("player_color")).count()
            return (wins / queryset.count()) * 100 if queryset.exists() else 0

        lower_games = games.filter(opponent__elo__lt=F("player__elo") - 10)
        similar_games = games.filter(
            opponent__elo__gte=F("player__elo") - 10,
            opponent__elo__lte=F("player__elo") + 10,
        )
        higher_games = games.filter(opponent__elo__gt=F("player__elo") + 10)

        return {
            "lower_ratio": win_ratio(lower_games),
            "similar_ratio": win_ratio(similar_games),
            "higher_ratio": win_ratio(higher_games),
        }

    def get_Xusername(self, games: QuerySet[Game]) -> str:
        if games[0].host == "lichess.org":
            return games[0].report.lichess_username
        if games[0].host == "chess.com":
            return games[0].report.chess_com_username

    def get_avg_time_per_move(self, games: QuerySet[Game]) -> list:
        """
        Your average time per move vs your opponent's average time per move.
        Statistic is calculated for each phase of the game. You can see
        when your opponent is spending more time than you and vice versa.
        </br>
        <b>
        If you see that:
        </b>
        <ul class="text-muted">
        <li>You are spending <code>more time in the opening</code> than your opponent,
        maybe you should learn more openings.</li>
        <li>You are spending <code>more time in the end game</code> than your opponent,
        maybe you should you should learn more end game theory.</li>
        <li>You are spending <code>more time in the middle game</code> than your opponent,
        maybe you should you should play more bullet games.</li>
        </ul>
        """
        avg_time = {
            "player": {"opening": 0, "middle_game": 0, "end_game": 0},
            "opponent": {"opening": 0, "middle_game": 0, "end_game": 0},
        }
        for game in games:
            for phase in ["opening", "middle_game", "end_game"]:
                try:
                    avg_time["player"][phase] += game.player.avg_move_time[phase]
                    avg_time["opponent"][phase] += game.opponent.avg_move_time[phase]
                except KeyError:
                    self.logger.error(
                        f"No {phase} in get_avg_time_per_move for game {game.id}"
                    )
                    break

        for phase in ["opening", "middle_game", "end_game"]:
            avg_time["player"][phase] /= games.count()
            avg_time["opponent"][phase] /= games.count()
        return avg_time

    def get_win_ratio_per_color(self, games: QuerySet[Game]) -> list:
        """
        Your win ratio as white vs your win ratio as black. <br/>
        """
        white = self.__get_win_ratio(Color.WHITE, games)
        black = self.__get_win_ratio(Color.BLACK, games)
        data_dict = {"white": white, "black": black}
        return data_dict

    def __get_win_ratio(self, color, games: QuerySet[Game]) -> int:
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        win = games.filter(
            report=self.report, player_color=color, result=F("player_color")
        ).count()
        lost = games.filter(
            report=self.report,
            player_color=color,
            result=opponent_color,
        ).count()
        draws = (
            games.filter(report=self.report, player_color=color).count() - win - lost
        )
        return [win, draws, lost]

    def get_win_ratio_per_opening_as_white(self, games: QuerySet[Game]) -> dict:
        """
        Your win ratio for each opening as white. <br/>
        You can see which openings are the most successful for you. <br/>
        """
        return self.__get_win_ratio_per_opening_for_color(games, Color.WHITE)

    def get_win_ratio_per_opening_as_black(self, games: QuerySet[Game]) -> dict:
        """
        Same as above but for black. <br/>
        """
        return self.__get_win_ratio_per_opening_for_color(games, Color.BLACK)

    def get_end_reasons(self, games: QuerySet[Game]) -> dict:
        """
        Reasons why the game ended. <br/>
        IMPORTANT: <b>Lichess Api does not provide this data.</b>
        """
        # field name end_reason
        end_reasons = {}
        end_reasons["win"] = list(
            games.filter(report=self.report, result=F("player_color"))
            .exclude(end_reason="unknown")
            .values("end_reason")
            .annotate(count=Count("end_reason"))
        )
        end_reasons["loss"] = list(
            games.filter(report=self.report)
            .exclude(
                Q(result=F("player_color"))
                | Q(result=Result.DRAW)
                | Q(end_reason="unknown")
            )
            .values("end_reason")
            .annotate(count=Count("end_reason"))
        )
        return end_reasons

    def __get_win_ratio_per_opening_for_color(
        self, games: QuerySet[Game], color: int, max_oppenings=5, short=True
    ) -> tuple[dict]:
        default_field_name = "opening"
        field_name = "opening"
        if short:
            field_name = "opening_short"
        openings = (
            games.filter(player_color=color)
            .values(field_name)
            .annotate(count=Count(field_name))
        )
        openings = sorted(openings, key=lambda x: x["count"], reverse=True)
        openings = openings[:max_oppenings]

        for opening in openings:
            opening[default_field_name] = opening.pop(field_name)
        win = Color.WHITE if color == Color.WHITE else Color.BLACK
        loss = Color.BLACK if color == Color.WHITE else Color.WHITE
        for opening in openings:
            for res, result in (("win", win), ("loss", loss), ("draw", Result.DRAW)):
                opening[res] = games.filter(
                    player_color=color,
                    opening__contains=opening[default_field_name],
                    result=result,
                ).count()
        return openings

    def get_player_elo_over_time(
        self, games: QuerySet[Game]
    ) -> list:  # TODO REfactor this method it retrurns 3 times the same data !!!
        """
        You can see how your elo changed over time. <br/>
        For most active players Lichess rating is about 200 points higher than chess.com rating.
        """
        games = games.annotate(count=Count("host")).order_by("-date")
        data = []
        day = -1
        for game in games:
            if game.date.date() != day:
                day = game.date.date()
                data.append({"x": game.date, "y": game.player.elo, "host": game.host})
        return data

    def get_mistakes_per_phase(self, games: QuerySet[Game]):
        """
        Mistakes that you made in each phase of the game. <br/>
        Keep in mind that this statistic is based on the engine evaluation. <br/>
        Higher engine depths means more accurate evaluation. <br/>
        """
        data = {}
        for phase_name in ["opening", "middle_game", "end_game"]:
            blunders, mistakes, inaccuracies = 0, 0, 0
            games_count = games.count()
            if games_count == 0:
                continue
            for game in games:
                inaccuracies += game.player.evaluation[phase_name]["inaccuracy"]
                mistakes += game.player.evaluation[phase_name]["mistake"]
                blunders += game.player.evaluation[phase_name]["blunder"]
            data[phase_name] = [
                inaccuracies / games_count,
                mistakes / games_count,
                blunders / games_count,
            ]
        return data
