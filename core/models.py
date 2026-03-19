from django.db import models


class Enterprise(models.Model):
    enterprise_name = models.CharField(max_length=255)
    organization_id = models.CharField(max_length=255)
    enterprise_id = models.CharField(max_length=255, unique=True)
    service_account_key_path = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.enterprise_name} ({self.enterprise_id})"
