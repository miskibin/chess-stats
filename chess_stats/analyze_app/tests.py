from django.test import TestCase
from django.urls import reverse
from .models import Report


class ReportModelTest(TestCase):
    def setUp(self):
        Report.objects.create(
            chess_com_username="testuser",
            lichess_username="testuser",
            time_class="rapid",
            games_num=10,
            engine_depth=10,
        )

    def test_report_content(self):
        report = Report.objects.get(id=1)
        expected_object_name = f"{report.chess_com_username}"
        self.assertEqual(expected_object_name, "testuser")


class ReportListViewTest(TestCase):
    def setUp(self):
        Report.objects.create(
            chess_com_username="testuser",
            lichess_username="testuser",
            time_class="rapid",
            games_num=10,
            engine_depth=10,
        )

    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get("/reports/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("report:report-list"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("report:report-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "reports.html")
