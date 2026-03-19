from django.contrib import admin, messages
from django.utils import timezone

from amapi.exceptions import AmapiServiceError
from amapi.services import amapi_service

from .models import Application, Device, Policy


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("app_name", "package_name", "install_type", "is_active", "updated_at")
    list_filter = ("install_type", "is_active")
    search_fields = ("app_name", "package_name")


@admin.action(description="Sync selected policies to AMAPI")
def sync_selected_policies(modeladmin, request, queryset):
    synced = 0
    failed = 0

    for policy in queryset:
        try:
            amapi_service.patch_policy(policy.policy_id, policy.payload)
            policy.sync_status = Policy.SyncStatus.SYNCED
            policy.last_sync_error = ""
            policy.last_synced_at = timezone.now()
            policy.save(update_fields=["sync_status", "last_sync_error", "last_synced_at", "updated_at"])
            synced += 1
        except AmapiServiceError as exc:
            policy.sync_status = Policy.SyncStatus.FAILED
            policy.last_sync_error = str(exc)
            policy.save(update_fields=["sync_status", "last_sync_error", "updated_at"])
            failed += 1

    if synced:
        messages.success(request, f"Synced policies: {synced}")
    if failed:
        messages.error(request, f"Failed policies: {failed}")


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ("name", "policy_id", "sync_status", "last_synced_at", "updated_at")
    list_filter = ("sync_status",)
    search_fields = ("name", "policy_id")
    filter_horizontal = ("applications",)
    actions = [sync_selected_policies]


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("device_id", "serial_number", "state", "policy", "last_seen_at", "updated_at")
    search_fields = ("device_id", "serial_number", "state")
    list_filter = ("state",)
