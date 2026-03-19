import os
from typing import Any

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from core.models import Enterprise

from .exceptions import AmapiServiceError


class AmapiService:
    SCOPE = ["https://www.googleapis.com/auth/androidmanagement"]

    def _get_enterprise(self) -> Enterprise:
        enterprise = Enterprise.objects.order_by("-updated_at").first()
        if not enterprise:
            raise AmapiServiceError("No enterprise configured.")
        return enterprise

    def _credentials_path(self, enterprise: Enterprise | None = None) -> str:
        if enterprise and enterprise.service_account_key_path:
            return enterprise.service_account_key_path
        path = settings.AMAPI_SERVICE_ACCOUNT_FILE
        if not path:
            raise AmapiServiceError("AMAPI_SERVICE_ACCOUNT_FILE is not configured.")
        return path

    def _client(self):
        enterprise = Enterprise.objects.order_by("-updated_at").first()
        key_path = self._credentials_path(enterprise)
        if not os.path.exists(key_path):
            raise AmapiServiceError(f"Service account key file not found: {key_path}")
        credentials = service_account.Credentials.from_service_account_file(key_path, scopes=self.SCOPE)
        return build("androidmanagement", "v1", credentials=credentials, cache_discovery=False)

    def _map_error(self, exc: Exception) -> AmapiServiceError:
        if isinstance(exc, HttpError):
            return AmapiServiceError(f"Google API error: {exc.status_code} {exc.reason}")
        return AmapiServiceError(str(exc))

    def create_signup_url(self) -> dict[str, Any]:
        try:
            client = self._client()
            request = client.signupUrls().create(
                projectId=settings.GOOGLE_CLOUD_PROJECT_ID,
                callbackUrl=settings.AMAPI_CALLBACK_URL,
            )
            return request.execute()
        except Exception as exc:
            raise self._map_error(exc) from exc

    def create_enterprise(self, enterprise_token: str, enterprise_name: str) -> dict[str, Any]:
        try:
            client = self._client()
            request = client.enterprises().create(
                projectId=settings.GOOGLE_CLOUD_PROJECT_ID,
                enterpriseToken=enterprise_token,
                body={"enterpriseDisplayName": enterprise_name},
            )
            return request.execute()
        except Exception as exc:
            raise self._map_error(exc) from exc

    def patch_policy(self, policy_id: str, policy_json: dict[str, Any]) -> dict[str, Any]:
        enterprise = self._get_enterprise()
        full_policy_name = f"{enterprise.enterprise_id}/policies/{policy_id}"
        payload = {**policy_json, "name": full_policy_name}

        try:
            client = self._client()
            request = client.enterprises().policies().patch(name=full_policy_name, body=payload)
            return request.execute()
        except Exception as exc:
            raise self._map_error(exc) from exc

    def create_enrollment_token(self, policy_id: str) -> dict[str, Any]:
        enterprise = self._get_enterprise()
        full_policy_name = f"{enterprise.enterprise_id}/policies/{policy_id}"

        body = {
            "policyName": full_policy_name,
            "duration": settings.AMAPI_TOKEN_DURATION,
        }

        try:
            client = self._client()
            request = client.enterprises().enrollmentTokens().create(parent=enterprise.enterprise_id, body=body)
            return request.execute()
        except Exception as exc:
            raise self._map_error(exc) from exc

    def get_device_status(self, device_id: str) -> dict[str, Any]:
        enterprise = self._get_enterprise()
        name = device_id if device_id.startswith("enterprises/") else f"{enterprise.enterprise_id}/devices/{device_id}"

        try:
            client = self._client()
            request = client.enterprises().devices().get(name=name)
            return request.execute()
        except Exception as exc:
            raise self._map_error(exc) from exc


amapi_service = AmapiService()
