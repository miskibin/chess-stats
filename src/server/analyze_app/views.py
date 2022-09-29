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
from pprint import pprint


class RaportCreateView(CreateView):
    model = models.Raport
    form_class = forms.RaportForm
    template_name = "create_raport.html"

    def post(self, request):
        form = forms.RaportForm(request.POST)
        async_task(
            get_games,
            form.data["username"],
            int(form.data["games_num"]),
            form.data["time_class"],
            int(form.data["engine_depth"]),
        )

        return redirect("raport:raport-list")

    def get_success_url(self):
        return reverse("raport:raport-list")

    def get_absolute_url(self):
        return reverse("raport:raport-list")


class RaportListView(ListView):
    template_name = "raports.html"
    queryset = models.Raport.objects.all()


class RaportDetailView(DetailView):
    template_name = "raport_detail.html"

    def get_object(self):
        id = self.kwargs.get("id")
        print(id)
        raport = get_object_or_404(models.Raport, id=id)
        games = models.ChessGame.objects.filter(raport=raport)
        print(games)
        return games

    def get_absolute_url(self):
        return reverse("raport:raport-detail", kwargs={"id": self.id})


class VisualizedRaportDetailView(DetailView):
    template_name = "raport_visualized.html"

    def get_object(self):
        id = self.kwargs.get("id")
        raport = get_object_or_404(models.Raport, id=id)
        win_ratio = queries.get_win_ratio_per_color(raport)
        openings = queries.get_win_ratio_per_oppening(raport)
        # mistakes = queries.get_mean_mistakes_num_per_phase(raport)
        pprint(win_ratio)
        return {"win_ratio": win_ratio}

    def get_absolute_url(self):
        return reverse("raport:raport-visualized", kwargs={"id": self.id})
