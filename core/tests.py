from django.test import TestCase
from django.urls import reverse

from .models import ContactSubmission


class WebsiteTests(TestCase):
    def test_homepage_renders_with_static_asset_urls(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/static/logo.png")
        self.assertContains(response, "/static/12808277_1080_1920_30fps.mp4")

    def test_valid_contact_submission_is_saved_and_redirected(self):
        response = self.client.post(
            reverse("home"),
            {
                "full_name": "Test Visitor",
                "organization": "Example Group",
                "email": "visitor@example.com",
                "inquiry_type": "strategic_partnership",
                "message": "We would like to discuss a partnership.",
                "website": "",
            },
        )
        self.assertRedirects(response, f"{reverse('home')}#contact")
        self.assertEqual(ContactSubmission.objects.count(), 1)

    def test_invalid_contact_submission_is_not_saved(self):
        response = self.client.post(reverse("home"), {"email": "not-an-email"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertContains(response, "Enter a valid email address.")

    def test_honeypot_submission_is_not_saved(self):
        response = self.client.post(
            reverse("home"),
            {
                "full_name": "Bot",
                "organization": "",
                "email": "bot@example.com",
                "inquiry_type": "capital_alignment",
                "message": "Automated message.",
                "website": "https://spam.example",
            },
        )
        self.assertRedirects(response, f"{reverse('home')}#contact")
        self.assertEqual(ContactSubmission.objects.count(), 0)
