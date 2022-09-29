from .models import Raport
from .models import ChessGame as Game
from django.db import models
from django.db.models import F


def get_win_ratio(raport: Raport, color) -> int:
    win, lost, draws = 0, 0, 0
    win = Game.objects.filter(
        raport=raport, player_color=color, result=F("player_color")
    ).count()
    lost = Game.objects.filter(
        raport=raport, player_color=color, result=1 - F("player_color")
    ).count()
    draws = Game.objects.filter(raport=raport, player_color=color, result=0.5).count()
    return [win, draws, lost]


def get_win_ratio_per_color(raport: Raport) -> list:
    white = get_win_ratio(raport, 0)
    black = get_win_ratio(raport, 1)
    return white + black


def get_win_ratio_per_oppening(raport: Raport, max_oppenings=5) -> list:
    openings = (
        Game.objects.filter(raport=raport)
        .values("opening")
        .annotate(count=models.Count("opening"))
    )
    openings = sorted(openings, key=lambda x: x["count"], reverse=True)
    openings = openings[:5]
    for opening in openings:
        opening["win"] = Game.objects.filter(
            raport=raport, opening=opening["opening"], result=F("player_color")
        ).count()
        opening["lost"] = Game.objects.filter(
            raport=raport, opening=opening["opening"], result=1 - F("player_color")
        ).count()
        opening["draws"] = Game.objects.filter(
            raport=raport, opening=opening["opening"], result=0.5
        ).count()
    return openings[:max_oppenings]
