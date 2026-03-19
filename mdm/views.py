import base64
from io import BytesIO

import qrcode
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from amapi.exceptions import AmapiServiceError
from amapi.services import amapi_service

from .models import Application, Device, Policy
from .serializers import ApplicationSerializer, DeviceSerializer, PolicySerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.order_by("app_name")
    serializer_class = ApplicationSerializer


class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.order_by("name")
    serializer_class = PolicySerializer

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        policy = self.get_object()
        try:
            response = amapi_service.patch_policy(policy.policy_id, policy.payload)
            policy.sync_status = Policy.SyncStatus.SYNCED
            policy.last_sync_error = ""
            policy.last_synced_at = timezone.now()
            policy.save(update_fields=["sync_status", "last_sync_error", "last_synced_at", "updated_at"])
            return Response({"status": "synced", "amapi": response})
        except AmapiServiceError as exc:
            policy.sync_status = Policy.SyncStatus.FAILED
            policy.last_sync_error = str(exc)
            policy.save(update_fields=["sync_status", "last_sync_error", "updated_at"])
            return Response({"status": "failed", "error": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

    @action(detail=True, methods=["post"], url_path="enrollment-token")
    def enrollment_token(self, request, pk=None):
        policy = self.get_object()
        try:
            token_payload = amapi_service.create_enrollment_token(policy.policy_id)
            qr_data = token_payload.get("qrCode") or token_payload.get("value", "")

            image = qrcode.make(qr_data)
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            png_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            return Response(
                {
                    "policy_id": policy.policy_id,
                    "token": token_payload,
                    "qr_data": qr_data,
                    "qr_image_base64": png_base64,
                }
            )
        except AmapiServiceError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.order_by("-updated_at")
    serializer_class = DeviceSerializer

    http_method_names = ["get", "post", "head", "options", "patch"]

    @action(detail=True, methods=["post"], url_path="refresh-status")
    def refresh_status(self, request, pk=None):
        device = self.get_object()
        try:
            payload = amapi_service.get_device_status(device.device_id)
            device.state = payload.get("state", "")
            device.raw_status = payload
            device.last_seen_at = timezone.now()
            device.save(update_fields=["state", "raw_status", "last_seen_at", "updated_at"])
            return Response({"status": "updated", "device": payload})
        except AmapiServiceError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
