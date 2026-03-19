from unittest.mock import MagicMock, patch

from django.test import TestCase

from core.models import Enterprise

from .exceptions import AmapiServiceError
from .services import AmapiService


class AmapiServiceTests(TestCase):
    def setUp(self):
        self.enterprise = Enterprise.objects.create(
            enterprise_name="Acme",
            organization_id="org-1",
            enterprise_id="enterprises/123",
            service_account_key_path="/tmp/key.json",
        )
        self.service = AmapiService()

    @patch("amapi.services.os.path.exists", return_value=True)
    @patch("amapi.services.service_account.Credentials.from_service_account_file")
    @patch("amapi.services.build")
    def test_patch_policy_success(self, build_mock, creds_mock, exists_mock):
        client = MagicMock()
        build_mock.return_value = client
        client.enterprises.return_value.policies.return_value.patch.return_value.execute.return_value = {"name": "p1"}

        result = self.service.patch_policy("policy-1", {"applications": []})
        self.assertEqual(result["name"], "p1")

    @patch.object(AmapiService, "_client", side_effect=Exception("boom"))
    def test_create_enrollment_token_error(self, _):
        with self.assertRaises(AmapiServiceError):
            self.service.create_enrollment_token("policy-1")
