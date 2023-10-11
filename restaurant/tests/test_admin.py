from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)
        self.cooker = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            years_of_experience=10,
        )

    def test_cooker_years_of_experience_listed(self):
        url = reverse("admin:restaurant_cook_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.cooker.years_of_experience)

    def test_cooker_years_of_experience_listed_on_detail_page(self):
        url = reverse(
            "admin:restaurant_cook_change", args=[self.cooker.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.cooker.years_of_experience)
