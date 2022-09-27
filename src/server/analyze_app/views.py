from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import models
from django_q.tasks import async_task, result


def home(request: HttpRequest) -> HttpResponse:
    raports = models.Raport.objects.all()
    return render(request, "home.html", {"raports": raports})


def raport(request: HttpRequest, pk: int) -> HttpResponse:
    raport = models.Raport.objects.get(pk=pk)
    games = models.ChessGame.objects.filter(raport=raport)
    return render(request, "raport.html", {"raport": raport, "games": games})


def create_raport(request: HttpRequest) -> HttpResponse:
    print("creating raport")
    task = async_task("analyze_app.tasks.get_games", "Barabasz60", 5, "rapid")

    print("creating raport")
    return render(request, "create_raport.html", {"task result": result(task)})
