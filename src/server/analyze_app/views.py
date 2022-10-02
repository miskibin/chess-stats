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
        raport = models.Raport(
            username=form.data["username"],
            time_class=form.data["time_class"],
            games_num=int(form.data["games_num"]),
            engine_depth=int(form.data["engine_depth"]),
        )
        raport.save()
        async_task(get_games, raport)
        return redirect(f"/{raport.id}/visualized")  # TODO CHANGE THIS TO REVERSE

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
        player_elo_over_time = queries.get_player_elo_over_time(raport)
        return {
            "username": raport.username,
            "win_ratio": win_ratio,
            "openings": openings,
            "elo_over_time": player_elo_over_time,
        }

    def get_absolute_url(self):
        return reverse("raport:raport-visualized", kwargs={"id": self.id})
