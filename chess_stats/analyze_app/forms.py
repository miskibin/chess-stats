from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
    time_class = forms.ChoiceField(
        choices=[("rapid", "rapid"), ("blitz", "blitz"), ("bullet", "bullet")],
        initial="blitz",
    )
    chess_com_username = forms.CharField(
        initial="Hikaru",
        max_length=40,
        required=False,
        help_text="leave blank if you don't want to analyze chess.com games",
    )
    lichess_username = forms.CharField(
        initial="DrNykterstein",
        max_length=40,
        required=False,
        help_text="leave blank if you don't want to analyze lichess.org games",
    )
    games_num = forms.IntegerField(
        initial=50,
        min_value=1,
        max_value=1000,
        help_text="number of games to analyze Must be divisible by number of hosts",
    )
    engine_depth = forms.IntegerField(initial=5)

    class Meta:
        model = Report
        fields = ("chess_com_username", "lichess_username", "games_num", "time_class")
