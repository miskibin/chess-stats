from .models import Report
from django import forms


class ReportForm(forms.ModelForm):
    time_class = forms.ChoiceField(
        choices=[("rapid", "rapid"), ("blitz", "blitz"), ("bullet", "bullet")],
        initial="rapid",
    )
    chess_com_username = forms.CharField(
        initial="Barabasz60",
        max_length=40,
        required=False,
        help_text="leave blank if you don't want to analyze chess.com games",
    )
    lichess_username = forms.CharField(
        initial="pro100wdupe",
        max_length=40,
        required=False,
        help_text="leave blank if you don't want to analyze lichess.org games",
    )
    games_num = forms.IntegerField(initial=50)
    engine_depth = forms.IntegerField(initial=5)

    class Meta:
        model = Report
        fields = ("chess_com_username", "lichess_username", "games_num", "time_class")
