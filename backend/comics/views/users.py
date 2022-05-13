from django.http import Http404
from rest_framework import views, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.request import Request

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
    def get_object(pk: int) -> User:
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: int, format=None) -> Response:
        user = self.get_object(pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        user = self.get_object(pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        user = self.get_object(pk)

        serializer = UserSerializer(self=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
