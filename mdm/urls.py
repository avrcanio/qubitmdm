from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet, DeviceViewSet, PolicyViewSet

router = DefaultRouter()
router.register(r"applications", ApplicationViewSet, basename="application")
router.register(r"policies", PolicyViewSet, basename="policy")
router.register(r"devices", DeviceViewSet, basename="device")

urlpatterns = router.urls
