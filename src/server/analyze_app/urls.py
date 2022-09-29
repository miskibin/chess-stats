from . import views
from django.urls import path

app_name = "raport"
urlpatterns = [
    path("", views.RaportListView.as_view(), name="raport-list"),
    path("create/", views.RaportCreateView.as_view(), name="raport-create"),
    path("<int:id>/", views.RaportDetailView.as_view(), name="raport-detail"),
    path(
        "<int:id>/visualized",
        views.VisualizedRaportDetailView.as_view(),
        name="raport-visualized",
    ),
    # path("<int:id>/games", views, name="raport-games"),
]
