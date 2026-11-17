import importlib
import os
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

import config.settings as settings_module

from .models import ContactSubmission


class WebsiteTests(TestCase):
    def test_homepage_renders_with_static_asset_urls(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/static/logo.png")
        self.assertContains(response, "/static/12808277_1080_1920_30fps.mp4")

    @patch("core.views.send_mail", return_value=1)
    def test_valid_contact_submission_is_saved_emailed_and_redirected(self, mocked_send_mail):
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
        mocked_send_mail.assert_called_once()
        self.assertEqual(mocked_send_mail.call_args.kwargs["recipient_list"], ["kkcorp524@gmail.com"])
        self.assertEqual(mocked_send_mail.call_args.kwargs["reply_to"], ["visitor@example.com"])

    @patch("core.views.send_mail", return_value=0)
    def test_email_failure_keeps_submission_and_reports_fallback(self, mocked_send_mail):
        response = self.client.post(
            reverse("home"),
            {
                "full_name": "Test Visitor",
                "organization": "",
                "email": "visitor@example.com",
                "inquiry_type": "strategic_partnership",
                "message": "We would like to discuss a partnership.",
                "website": "",
            },
            follow=True,
        )
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertContains(response, "Your inquiry was saved, but we couldn&#x27;t email it right now.")
        mocked_send_mail.assert_called_once()

    def test_invalid_contact_submission_is_not_saved(self):
        response = self.client.post(reverse("home"), {"email": "not-an-email"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertContains(response, "Please enter a valid email address.")

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

    def test_missing_environment_defaults_to_local_development_settings(self):
        with patch.dict(os.environ, {}, clear=True), patch("dotenv.load_dotenv", return_value=False):
            reloaded = importlib.reload(settings_module)
            self.assertTrue(reloaded.DEBUG)
            self.assertTrue(reloaded.SECRET_KEY)
