from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from core.views import health_live, health_ready

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/live/", health_live, name="health-live"),
    path("health/ready/", health_ready, name="health-ready"),
    path("api/auth/token/", obtain_auth_token, name="api-token"),
    path("api/", include("mdm.urls")),
    path("api/", include("core.urls")),
]
