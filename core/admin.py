from django.contrib import admin

from .models import Enterprise


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ("enterprise_name", "organization_id", "enterprise_id", "updated_at")
    search_fields = ("enterprise_name", "organization_id", "enterprise_id")
