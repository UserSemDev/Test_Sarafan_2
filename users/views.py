from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import UserSerializer, UserModifySerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return UserSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return UserModifySerializer
        return super().get_serializer_class()
