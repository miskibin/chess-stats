from .models import Report
from .models import ChessGame as Game
from django.db import models
from django.db.models import F


def get_win_ratio(report: Report, color) -> int:
    win, lost, draws = 0, 0, 0
    win = Game.objects.filter(
        report=report, player_color=color, result=F("player_color")
    ).count()
    lost = Game.objects.filter(
        report=report, player_color=color, result=1 - F("player_color")
    ).count()
    draws = Game.objects.filter(report=report, player_color=color, result=0.5).count()
    return [win, draws, lost]


def get_win_ratio_per_color(report: Report) -> list:
    white = get_win_ratio(report, 0)
    black = get_win_ratio(report, 1)
    return white + black


def get_player_elo_over_time(report: Report) -> list:
    games = Game.objects.filter(report=report).order_by("-date")
    data = []
    day = games[0].date.day
    for game in games:
        if game.date.day != day:
            day = game.date.day
            data.append({"x": game.date, "y": game.player_elo})
    return data


def get_win_ratio_per_oppening(report: Report, max_oppenings=5) -> list:
    openings = (
        Game.objects.filter(report=report)
        .values("opening")
        .annotate(count=models.Count("opening"))
    )
    openings = sorted(openings, key=lambda x: x["count"], reverse=True)
    openings = openings[:max_oppenings]
    for opening in openings:
        opening["win"] = Game.objects.filter(
            report=report, opening=opening["opening"], result=F("player_color")
        ).count()
        opening["lost"] = Game.objects.filter(
            report=report, opening=opening["opening"], result=1 - F("player_color")
        ).count()
        opening["draws"] = Game.objects.filter(
            report=report, opening=opening["opening"], result=0.5
        ).count()
    return openings
