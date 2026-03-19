import os

from django.core.checks import Error, register
from django.db import connection
from django.db.utils import OperationalError


@register()
def amapi_startup_checks(app_configs, **kwargs):
    errors = []

    required = ["GOOGLE_CLOUD_PROJECT_ID", "AMAPI_SERVICE_ACCOUNT_FILE"]
    for key in required:
        if not os.getenv(key):
            errors.append(Error(f"Missing required environment variable: {key}", id="core.E001"))

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except OperationalError as exc:
        errors.append(Error(f"Database connectivity issue: {exc}", id="core.E002"))

    return errors
