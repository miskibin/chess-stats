from django.test import TestCase
from django.urls import reverse
from ..models import Report


class ReportListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 10 reports for pagination tests
        for i in range(10):
            Report.objects.create(
                chess_com_username=f"testuser{i}",
                lichess_username=f"testuser{i}",
                time_class="blitz",
                games_num=2,
                engine_depth=10,
            )

    def test_FR10_view_url_exists_at_desired_location(self):
        response = self.client.get("/reports/")
        self.assertEqual(response.status_code, 200)

    def test_FR10_view_url_accessible_by_name(self):
        response = self.client.get(reverse("report:report-list"))
        self.assertEqual(response.status_code, 200)

    def test_FR10_view_uses_correct_template(self):
        response = self.client.get(reverse("report:report-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reports.html")

    def test_FR10_pagination_is_ten(self):
        response = self.client.get(reverse("report:report-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == False)
