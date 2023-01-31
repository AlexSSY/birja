from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .serializers import StakeModelSerializer
from .models import StakeModel
from .filters import IsOwnerFilterBackend


class StakeModelAPIView(ModelViewSet):
    queryset = StakeModel.objects.all()
    serializer_class = StakeModelSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [IsOwnerFilterBackend, SearchFilter]
    search_fields = ['=stake_period', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)