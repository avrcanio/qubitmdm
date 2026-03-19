from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Application, Policy


class AuthAndPolicyTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="api", password="secret12345")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_application_crud_create(self):
        url = reverse("application-list")
        response = self.client.post(
            url,
            {
                "package_name": "com.example.app",
                "app_name": "Example",
                "install_type": Application.InstallType.ALLOWED,
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    @patch("mdm.views.amapi_service.patch_policy")
    def test_policy_sync_success(self, patch_policy):
        patch_policy.return_value = {"name": "ok"}
        policy = Policy.objects.create(name="Policy 1", policy_id="policy-1", payload={"applications": []})

        url = reverse("policy-sync", kwargs={"pk": policy.pk})
        response = self.client.post(url)
        policy.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(policy.sync_status, Policy.SyncStatus.SYNCED)

    @patch("mdm.views.amapi_service.create_enrollment_token")
    def test_enrollment_token_success(self, create_token):
        create_token.return_value = {"value": "token-123", "qrCode": "sample-qr"}
        policy = Policy.objects.create(name="Policy 2", policy_id="policy-2", payload={})

        url = reverse("policy-enrollment-token", kwargs={"pk": policy.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("qr_image_base64", response.json())
