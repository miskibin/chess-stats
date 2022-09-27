from django.db import models


class Raport(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=100)
    time_class = models.CharField(max_length=100)
    games_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ChessGame(models.Model):
    raport = models.ForeignKey(Raport, on_delete=models.CASCADE)
    player_elo = models.IntegerField(null=True, help_text="Player's ELO")
    opponent_elo = models.IntegerField(null=True, help_text="Opponent's ELO")
    opening = models.CharField(max_length=100, null=True, help_text="Opening name")
    result = models.CharField(max_length=10, help_text="Result of the game")
    date = models.DateField(help_text="Date of the game")
    time_control = models.CharField(max_length=20, help_text="Time control of the game")
    player_color = models.CharField(
        max_length=10, help_text="Player's color 0-White, 1-Black"
    )
    mean_player_time_per_move = models.IntegerField(
        null=True, help_text="Mean player time per move"
    )
    mean_opponent_time_per_move = models.IntegerField(
        null=True, help_text="Mean opponent time per move"
    )
    moves = models.IntegerField(help_text="Number of moves in the game")
    time_class = models.CharField(max_length=10, help_text="eg. rapid, blitz, bullet")
    phases = models.JSONField(help_text="list with phases of the game")
    mistakes = models.JSONField(
        help_text="mistakes of the player in phases of the game"
    )
    created = models.DateTimeField(auto_now_add=True)
