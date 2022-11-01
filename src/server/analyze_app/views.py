from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from . import models, forms, queries
from .tasks import get_games, convert_data
from django_q.tasks import async_task, result
from django.views.generic import CreateView
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    ListView,
)


class ReportCreateView(CreateView):
    model = models.Report
    form_class = forms.ReportForm
    template_name = "create_report.html"

    def post(self, request):
        form = forms.ReportForm(request.POST)
        report = models.Report(
            username=form.data["username"],
            time_class=form.data["time_class"],
            games_num=int(form.data["games_num"]),
            engine_depth=int(form.data["engine_depth"]),
        )
        report.save()
        async_task(get_games, report)
        return redirect(f"/{report.pk}/visualized")  # TODO CHANGE THIS TO REVERSE

    def get_absolute_url(self):
        return reverse("report:report-list")


class ReportListView(ListView):
    template_name = "reports.html"
    queryset = models.Report.objects.all()


class ReportDetailView(DetailView):
    template_name = "report_detail.html"

    def get_object(self):
        id = self.kwargs.get("id")
        print(id)
        report = get_object_or_404(models.Report, id=id)
        games = models.ChessGame.objects.filter(report=report)
        return games

    def get_absolute_url(self):
        return reverse("report:report-detail", kwargs={"id": self.id})


class VisualizedReportDetailView(DetailView):
    template_name = "report_visualized.html"

    def get_object(self):
        if not models.ChessGame.objects.filter(report=self.kwargs.get("id")).exists():
            return {}
        id = self.kwargs.get("id")
        report = get_object_or_404(models.Report, id=id)
        win_ratio = queries.get_win_ratio_per_color(report)
        openings_per_color = queries.get_win_ratio_per_opening(report)
        player_elo_over_time = queries.get_player_elo_over_time(report)
        return {
            "username": report.username,
            "win_ratio": win_ratio,
            "openings_per_color": openings_per_color,
            "elo_over_time": player_elo_over_time,
        }

    def get_absolute_url(self):
        return reverse("report:report-visualized", kwargs={"id": self.id})
