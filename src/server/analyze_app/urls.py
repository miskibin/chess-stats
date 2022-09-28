from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("raport/<int:pk>/", views.raport, name="raport"),
    path("raport/create", views.create_raport, name="create_raport"),
]
