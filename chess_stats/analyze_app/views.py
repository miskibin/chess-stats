from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django_q.tasks import async_task
from easy_logs import get_logger

from . import forms, models, queries
from .tasks import get_games

LOGGER = get_logger(lvl="DEBUG")


class IndexView(TemplateView):
    template_name = "index.html"

    # def get_absolute_url(self):
    #     return reverse("report:report-detail", kwargs={"id": self.id})


class ReportCreateView(CreateView):
    model = models.Report
    form_class = forms.ReportForm
    template_name = "create_report.html"

    def post(self, request):
        form = forms.ReportForm(request.POST)
        report = models.Report(
            chess_com_username=form.data["chess_com_username"],
            lichess_username=form.data["lichess_username"],
            time_class=form.data["time_class"],
            games_num=int(form.data["games_num"]),
            engine_depth=int(form.data["engine_depth"]),
        )
        report.save()
        async_task(get_games, report)
        return redirect(f"/{report.pk}/visualized")  # TODO CHANGE THIS TO REVERSE

    def get_absolute_url(self):
        return reverse("report:report-list")


class ReportDeleteView(DetailView):
    def get_object(self):
        _id = self.kwargs.get("id")
        report = get_object_or_404(models.Report, id=_id)
        return report

    def post(self, request, *args, **kwargs):
        _id = self.kwargs.get("id")
        report = get_object_or_404(models.Report, id=_id)
        report.delete()
        return redirect("report:report-list")


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
    template_name = "visualized_wraper.html"

    def get_object(self):
        id = self.kwargs.get("id")
        report = get_object_or_404(models.Report, id=id)
        if not models.ChessGame.objects.filter(report=self.kwargs.get("id")).exists():
            return {
                "Xanalyzed_games": {
                    "total": report.analyzed_games,
                },
                "Xfail_reason": report.fail_reason,
            }
        queries_maker = queries.QueriesMaker(report, LOGGER)
        data = queries_maker.asdict()
        # conclusion_maker = ConclusionsMaker(data, LOGGER)
        # conclusions = conclusion_maker.asdict()
        # merge dicts
        # return {**data, **conclusions}
        return data

    def get_absolute_url(self):
        return reverse("report:report-visualized", kwargs={"id": self.id})
