from .models import Report
from django import forms


class ReportForm(forms.ModelForm):
    time_class = forms.ChoiceField(
        choices=[("rapid", "rapid"), ("blitz", "blitz"), ("bullet", "bullet")],
        initial="rapid",
    )
    username = forms.CharField(initial="Barabasz60", max_length=40)
    games_num = forms.IntegerField(initial=50)
    engine_depth = forms.IntegerField(initial=5)

    class Meta:
        model = Report
        fields = ("username", "games_num", "time_class")
