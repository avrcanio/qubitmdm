from rest_framework.routers import DefaultRouter

from .views_api import EnterpriseViewSet

router = DefaultRouter()
router.register(r"enterprises", EnterpriseViewSet, basename="enterprise")

urlpatterns = router.urls
