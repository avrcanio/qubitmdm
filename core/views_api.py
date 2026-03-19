from rest_framework import viewsets

from .models import Enterprise
from .serializers import EnterpriseSerializer


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.order_by("-updated_at")
    serializer_class = EnterpriseSerializer
