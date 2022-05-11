from rest_framework import views, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.exceptions import ObjectDoesNotExist

from ..models import User
from ..serializers import UserSerializer


class UserList(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request: Request, format=None) -> Response:
        queryset = User.objects.all()
        serializer = UserSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class UserCreate(views.APIView):
    @staticmethod
    def post(request: Request, format=None) -> Response:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(views.APIView):
    @staticmethod
    def get(request: Request, pk: int, format=None) -> Response:

        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)

    @staticmethod
    def delete(request: Request, pk: int, format=None) -> Response:
        User.objects.get(pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        ...
