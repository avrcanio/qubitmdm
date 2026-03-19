from rest_framework import serializers

from .models import Enterprise


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
