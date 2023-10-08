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


from django.db import models


# Generated basing on chess-insight readme
class ChessGame(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="games", null=True
    )
    date = models.DateTimeField(help_text="Date and time of the game in UTC.")
    host = models.CharField(
        max_length=255, help_text="Server where the game was played."
    )
    opening = models.CharField(
        max_length=255, help_text="Full opening name in ECO format."
    )
    opening_short = models.CharField(
        max_length=255, help_text="Short opening name in ECO format."
    )
    opponent_avg_move_time_opening = models.FloatField(
        help_text="Opponent's average move time in the opening phase."
    )
    opponent_avg_move_time_middle_game = models.FloatField(
        help_text="Opponent's average move time in the middle game phase."
    )
    opponent_avg_move_time_end_game = models.FloatField(
        help_text="Opponent's average move time in the end game phase."
    )
    opponent_elo = models.IntegerField(help_text="Opponent's Elo rating.")
    opponent_inaccuracy_opening = models.IntegerField(
        help_text="Number of inaccuracies made by the opponent in the opening phase."
    )
    opponent_mistake_opening = models.IntegerField(
        help_text="Number of mistakes made by the opponent in the opening phase."
    )
    opponent_blunder_opening = models.IntegerField(
        help_text="Number of blunders made by the opponent in the opening phase."
    )
    opponent_inaccuracy_middle_game = models.IntegerField(
        help_text="Number of inaccuracies made by the opponent in the middle game phase."
    )
    opponent_mistake_middle_game = models.IntegerField(
        help_text="Number of mistakes made by the opponent in the middle game phase."
    )
    opponent_blunder_middle_game = models.IntegerField(
        help_text="Number of blunders made by the opponent in the middle game phase."
    )
    opponent_inaccuracy_end_game = models.IntegerField(
        help_text="Number of inaccuracies made by the opponent in the end game phase."
    )
    opponent_mistake_end_game = models.IntegerField(
        help_text="Number of mistakes made by the opponent in the end game phase."
    )
    opponent_blunder_end_game = models.IntegerField(
        help_text="Number of blunders made by the opponent in the end game phase."
    )
    phases_opening = models.IntegerField(
        help_text="Number of half moves in the opening phase."
    )
    phases_middle_game = models.IntegerField(
        help_text="Number of half moves in the middle game phase."
    )
    phases_end_game = models.IntegerField(
        help_text="Number of half moves in the end game phase."
    )
    player_avg_move_time_opening = models.FloatField(
        help_text="Player's average move time in the opening phase."
    )
    player_avg_move_time_middle_game = models.FloatField(
        help_text="Player's average move time in the middle game phase."
    )
    player_avg_move_time_end_game = models.FloatField(
        help_text="Player's average move time in the end game phase."
    )
    player_elo = models.IntegerField(help_text="Player's Elo rating.")
    player_inaccuracy_opening = models.IntegerField(
        help_text="Number of inaccuracies made by the player in the opening phase."
    )
    player_mistake_opening = models.IntegerField(
        help_text="Number of mistakes made by the player in the opening phase."
    )
    player_blunder_opening = models.IntegerField(
        help_text="Number of blunders made by the player in the opening phase."
    )
    player_inaccuracy_middle_game = models.IntegerField(
        help_text="Number of inaccuracies made by the player in the middle game phase."
    )
    player_mistake_middle_game = models.IntegerField(
        help_text="Number of mistakes made by the player in the middle game phase."
    )
    player_blunder_middle_game = models.IntegerField(
        help_text="Number of blunders made by the player in the middle game phase."
    )
    player_inaccuracy_end_game = models.IntegerField(
        help_text="Number of inaccuracies made by the player in the end game phase."
    )
    player_mistake_end_game = models.IntegerField(
        help_text="Number of mistakes made by the player in the end game phase."
    )
    player_blunder_end_game = models.IntegerField(
        help_text="Number of blunders made by the player in the end game phase."
    )
    player_color = models.CharField(
        max_length=10, help_text="Player's color in the game."
    )
    result_winner = models.CharField(
        max_length=10,
        help_text="The winner of the game (e.g., 'white', 'black', or 'draw').",
    )
    result_reason = models.CharField(
        max_length=255, help_text="The reason for the game result."
    )
    time_class = models.CharField(
        max_length=50, help_text="The time class of the game."
    )
    time_control = models.CharField(
        max_length=20,
        help_text="The time control format in seconds (e.g., '600+0' or '180+2').",
    )
    url = models.URLField(max_length=255, help_text="URL to the game.")
    username = models.CharField(max_length=255, help_text="Username of the player.")

    def __str__(self):
        return f"{self.date} - {self.username} url: {self.url}"
