from pathlib import Path
from tempfile import NamedTemporaryFile

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

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


class BootstrapEnterpriseCommandTests(TestCase):
    @patch("core.management.commands.bootstrap_enterprise.amapi_service.create_enterprise")
    def test_enterprise_token_requires_signup_url_name(self, create_enterprise_mock):
        with self.assertRaisesMessage(CommandError, "Provide --signup-url-name when using --enterprise-token."):
            call_command(
                "bootstrap_enterprise",
                enterprise_token="token-1",
                service_account_key_path="/run/secrets/amapi-service-account.json",
            )
        create_enterprise_mock.assert_not_called()

    @patch("core.management.commands.bootstrap_enterprise.amapi_service.create_enterprise")
    def test_enterprise_saved_when_signup_url_name_provided(self, create_enterprise_mock):
        create_enterprise_mock.return_value = {"name": "enterprises/LC011hne7m"}

        call_command(
            "bootstrap_enterprise",
            enterprise_token="token-1",
            signup_url_name="signupUrls/Cf99dedb65dca740f",
            enterprise_name="QubitMDM Enterprise",
            organization_id="default-org",
            service_account_key_path="/run/secrets/amapi-service-account.json",
        )

        enterprise = Enterprise.objects.get(enterprise_id="enterprises/LC011hne7m")
        self.assertEqual(enterprise.enterprise_name, "QubitMDM Enterprise")
        create_enterprise_mock.assert_called_once_with(
            enterprise_token="token-1",
            enterprise_name="QubitMDM Enterprise",
            signup_url_name="signupUrls/Cf99dedb65dca740f",
        )
