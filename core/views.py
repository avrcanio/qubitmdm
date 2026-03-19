import os
from pathlib import Path

from django.db import connection
from django.db.utils import OperationalError
from django.http import JsonResponse

from .models import Enterprise


def health_live(request):
    return JsonResponse({"status": "ok"})


def health_ready(request):
    checks = {
        "database": False,
        "enterprise": False,
        "service_account_file": False,
    }

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = True
    except OperationalError:
        pass

    enterprise = Enterprise.objects.order_by("-updated_at").first()
    checks["enterprise"] = bool(enterprise)

    if enterprise and enterprise.service_account_key_path:
        checks["service_account_file"] = Path(enterprise.service_account_key_path).exists()
    else:
        env_path = os.getenv("AMAPI_SERVICE_ACCOUNT_FILE", "")
        checks["service_account_file"] = bool(env_path and Path(env_path).exists())

    ready = all(checks.values())
    return JsonResponse({"status": "ready" if ready else "not_ready", "checks": checks}, status=200 if ready else 503)
