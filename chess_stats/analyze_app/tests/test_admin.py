from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.contrib.auth.models import User
from analyze_app.admin import ReportAdmin
from analyze_app.models import Report


class MockRequest:
    pass


class ReportAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = ReportAdmin(Report, self.site)
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            "admin", "admin@test.com", "password"
        )
        self.client.login(username="admin", password="password")

    def test_FR11_admin_list_display(self):
        list_display = (
            "chess_com_username",
            "lichess_username",
            "time_class",
            "games_num",
            "analyzed_games",
            "engine_depth",
            "fail_reason",
            "professional",
        )
        self.assertEqual(self.admin.list_display, list_display)

    def test_FR11_admin_add_report(self):
        response = self.client.post(
            "/admin/analyze_app/report/add/",
            {
                "chess_com_username": "testuser",
                "lichess_username": "testuser",
                "time_class": "blitz",
                "games_num": 2,
                "engine_depth": 10,
                "analyzed_games": 5,
                "fail_reason": "None",
                "professional": False,
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        self.assertEqual(Report.objects.count(), 1)

    def test_FR11_admin_search_fields(self):
        search_fields = ("chess_com_username", "lichess_username")
        self.assertEqual(self.admin.search_fields, search_fields)

    def test_FR11_admin_access(self):
        response = self.client.get("/admin/analyze_app/report/")
        self.assertEqual(response.status_code, 200)
