from django.db import models


class Application(models.Model):
    class InstallType(models.TextChoices):
        FORCE_INSTALLED = "FORCE_INSTALLED", "Force Installed"
        ALLOWED = "ALLOWED", "Allowed"
        BLOCKED = "BLOCKED", "Blocked"

    package_name = models.CharField(max_length=255, unique=True)
    app_name = models.CharField(max_length=255)
    install_type = models.CharField(max_length=32, choices=InstallType.choices, default=InstallType.ALLOWED)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.app_name} ({self.package_name})"


class Policy(models.Model):
    class SyncStatus(models.TextChoices):
        NEVER_SYNCED = "NEVER_SYNCED", "Never Synced"
        SYNCED = "SYNCED", "Synced"
        FAILED = "FAILED", "Failed"

    name = models.CharField(max_length=255)
    policy_id = models.CharField(max_length=255, unique=True)
    payload = models.JSONField(default=dict)
    applications = models.ManyToManyField(Application, blank=True, related_name="policies")
    sync_status = models.CharField(max_length=32, choices=SyncStatus.choices, default=SyncStatus.NEVER_SYNCED)
    last_sync_error = models.TextField(blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    device_id = models.CharField(max_length=255, unique=True)
    serial_number = models.CharField(max_length=255, blank=True)
    policy = models.ForeignKey(Policy, null=True, blank=True, on_delete=models.SET_NULL, related_name="devices")
    state = models.CharField(max_length=255, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    raw_status = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.device_id
