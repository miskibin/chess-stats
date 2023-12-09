from django.test import TestCase, Client
from django.urls import reverse
from ..models import Report


class ReportCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_report_url = reverse("report:report-create")

    def test_FR6_create_report(self):
        response = self.client.post(
            self.create_report_url,
            {
                "chess_com_username": "testuser",
                "lichess_username": "testuser",
                "time_class": "rapid",
                "games_num": 10,
                "engine_depth": 10,
            },
        )
        self.assertEqual(response.status_code, 302)  # Check if redirect
        self.assertEqual(Report.objects.count(), 1)  # Check if report created
        report = Report.objects.first()
        self.assertEqual(report.chess_com_username, "testuser")
        self.assertEqual(report.lichess_username, "testuser")
        self.assertEqual(report.time_class, "rapid")
        self.assertEqual(report.games_num, 10)

    def test_FR7_create_amateur_and_professional_reports(self):
        # Create professional report
        response = self.client.post(
            self.create_report_url,
            {
                "chess_com_username": "testuserpro",
                "lichess_username": "testuserpro",
                "time_class": "rapid",
                "games_num": 10,
                "engine_depth": 10,
                "professional": True,
            },
        )
        self.assertEqual(response.status_code, 302)  # Check if redirect
        self.assertEqual(Report.objects.count(), 1)  # Check if report created
        professional_report = Report.objects.last()
        self.assertEqual(professional_report.professional, True)
