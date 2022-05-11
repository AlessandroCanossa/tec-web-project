from django.http import HttpRequest
from rest_framework import views
from rest_framework.response import Response
from rest_framework import authentication, permissions

from ..models import User
from ..serializers import UserSerializer


class UserList(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request: HttpRequest, format=None) -> Response:
        queryset = User.objects.all()
        serializer = UserSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class UserDetails(views.APIView):
    # permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request: HttpRequest, pk: int, format=None) -> Response:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
