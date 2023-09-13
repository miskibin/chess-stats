from django.db import models


class Report(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    chess_com_username = models.CharField(max_length=100)
    lichess_username = models.CharField(max_length=100)
    time_class = models.CharField(max_length=20)
    games_num = models.IntegerField()
    analyzed_games = models.IntegerField(default=0, null=True)
    engine_depth = models.IntegerField(default=10)
    fail_reason = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.chess_com_username + " " + self.lichess_username


class ChessGame(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    player_elo = models.IntegerField(null=True, help_text="Player's ELO")
    opponent_elo = models.IntegerField(null=True, help_text="Opponent's ELO")
    opening = models.CharField(max_length=70, null=True, help_text="Opening name")
    host = models.CharField(
        max_length=20, null=True, help_text="Site name eg. chess.com, lichess"
    )
    short_opening = models.CharField(
        max_length=40, null=True, help_text="Short opening name"
    )
    result = models.FloatField(
        choices=[(0, "white"), (1, "black"), (0.5, "draw")], max_length=10
    )
    date = models.DateTimeField(help_text="Date of the game")
    time_control = models.CharField(max_length=20, help_text="Time control of the game")
    player_color = models.IntegerField(
        choices=[(0, "white"), (1, "black")],
        help_text="Player's color 0-White, 1-Black",
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
    player_mistakes = models.JSONField(
        help_text="mistakes of the player in phases of the game"
    )
    opponent_mistakes = models.JSONField(
        help_text="mistakes of the opponent in phases of the game"
    )
    created = models.DateTimeField(auto_now_add=True)
