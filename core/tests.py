from pathlib import Path
from tempfile import NamedTemporaryFile

from django.test import TestCase
from django.urls import reverse

from .models import Enterprise


class HealthReadyTests(TestCase):
    def test_ready_fails_without_enterprise(self):
        response = self.client.get(reverse("health-ready"))
        self.assertEqual(response.status_code, 503)
        self.assertFalse(response.json()["checks"]["enterprise"])

    def test_ready_passes_with_enterprise_and_key(self):
        with NamedTemporaryFile() as temp_key:
            Enterprise.objects.create(
                enterprise_name="Acme",
                organization_id="org-1",
                enterprise_id="enterprises/123",
                service_account_key_path=temp_key.name,
            )
            response = self.client.get(reverse("health-ready"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ready")
