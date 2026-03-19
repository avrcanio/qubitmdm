from rest_framework import serializers

from .models import Application, Device, Policy


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class PolicySerializer(serializers.ModelSerializer):
    applications = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all(), many=True, required=False)

    class Meta:
        model = Policy
        fields = "__all__"
        read_only_fields = ("sync_status", "last_sync_error", "last_synced_at", "created_at", "updated_at")


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
