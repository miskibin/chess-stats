from django.urls import path

from . import views

app_name = "report"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("reports/", views.ReportListView.as_view(), name="report-list"),
    path("create/", views.ReportCreateView.as_view(), name="report-create"),
    path("<int:id>/", views.ReportDetailView.as_view(), name="report-detail"),
    path(
        "<int:id>/visualized",
        views.VisualizedReportDetailView.as_view(),
        name="report-visualized",
    ),
    path("<int:id>/delete", views.ReportDeleteView.as_view(), name="report-delete"),
    # path("<int:id>/games", views, name="report-games"),
]
