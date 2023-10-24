from collections.abc import Iterable
from django.db import models, transaction


class Color(models.TextChoices):
    WHITE = "white"
    BLACK = "black"


class Result(models.TextChoices):
    WHITE = Color.WHITE
    DRAW = "draw"
    BLACK = Color.BLACK


class Report(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    chess_com_username = models.CharField(max_length=100)
    lichess_username = models.CharField(max_length=100)
    time_class = models.CharField(max_length=20)
    games_num = models.IntegerField()
    analyzed_games = models.IntegerField(default=0, null=True)
    engine_depth = models.IntegerField(default=10)
    fail_reason = models.CharField(max_length=100, null=True, blank=True)
    professional = models.BooleanField(default=False)

    def __str__(self):
        return self.chess_com_username + " " + self.lichess_username


class SingleGamePlayer(models.Model):
    evaluation = models.JSONField(help_text="Evaluation of the player per phase.")
    elo = models.IntegerField(help_text="ELO rating of the player.")
    avg_move_time = models.JSONField(
        help_text="Average move time of the player per phase."
    )


# Generated basing on chess-insight readme
class ChessGame(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="games", null=True
    )
    player = models.ForeignKey(
        SingleGamePlayer,
        on_delete=models.CASCADE,
        related_name="player",
        help_text="Player object.",
    )
    opponent = models.ForeignKey(
        SingleGamePlayer,
        on_delete=models.CASCADE,
        related_name="opponent",
        help_text="Opponent object.",
    )

    date = models.DateTimeField(help_text="Date and time of the game in UTC.")
    host = models.CharField(
        max_length=255, help_text="Server where the game was played."
    )
    opening = models.CharField(max_length=255, help_text="Opening name in ECO format.")
    opening_short = models.CharField(
        max_length=50, help_text="Short opening name in ECO format."
    )

    phases = models.JSONField(
        help_text="Phases in half moves in the format (opening, middle game, end game)."
    )

    player_color = models.CharField(
        max_length=10, help_text="Player color in the game.", choices=Color.choices
    )
    result = models.CharField(max_length=60, choices=Result.choices)
    end_reason = models.CharField(
        max_length=50, help_text="Reason of the game end. e.g., 'checkmate'"
    )
    time_class = models.CharField(max_length=50, help_text="Time class of the game.")
    time_control = models.CharField(
        max_length=50,
        help_text="Time control in the format 'time+increment' in seconds. e.g., '600+0' or '180+2'",
    )
    url = models.URLField(help_text="URL to the game.")
    username = models.CharField(max_length=50, help_text="Username of the player.")

    def save(self, *args, **kwargs):
        # Create savepoints before saving objects
        with transaction.atomic():
            if not self.player.pk:
                self.player.save()
            if not self.opponent.pk:
                self.opponent.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.username} url: {self.url}"
