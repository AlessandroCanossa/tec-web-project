from django.http import Http404
from rest_framework import views, status, authentication, permissions, generics
from rest_framework.response import Response
from rest_framework.request import Request

from ..models import User
from ..serializers import UserSerializer, UserCreateSerializer


class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


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

        if user.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        user = self.get_object(pk)

        if user.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
