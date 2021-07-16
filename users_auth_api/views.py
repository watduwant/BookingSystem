from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .permissions import IsLoggedInUserOrAdmin
from .models import User
from datetime import datetime, timedelta

# Create your views here.
from .serializers import UserSerializer, UserTrialSerializer, UserStockPermissionsSerializer
import requests


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Permissions
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@api_view()
def UserSubscribedViewSet(request):
    user = request.user

    data = [
        {
            "django_tutorial_subscription": user.profile.django_tutorial_subscription,
            "angular_tutorial_subscription": user.profile.angular_tutorial_subscription,
            "django_project_subscription": user.profile.django_project_subscription,
            "angular_project_subscription": user.profile.angular_project_subscription,
        }
    ]

    serializer = UserTrialSerializer(data, many=True)

    return Response(serializer.data)

@api_view()
def UserStockPermissionsViewSet(request):
    user = request.user
    data = [
        {
            "permissions": user.profile.permissions,

        }
    ]

    serializer = UserStockPermissionsSerializer(data, many=True)

    return Response(serializer.data)

