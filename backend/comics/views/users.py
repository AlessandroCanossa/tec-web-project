from django.http import Http404
from rest_framework import views, status, permissions, generics
from rest_framework.response import Response
from rest_framework.request import Request

from ..models import User, Library, Market, Comment, ReadHistory, BuyList
from ..serializers import *


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


class LibraryList(views.APIView):
    def get(self, request: Request, user_id: int, format=None) -> Response:
        library = Library.objects.filter(user_id=user_id)
        serializer = LibrarySerializer(library, many=True, context={'request': request})
        return Response(serializer.data)


class LibraryAdd(generics.CreateAPIView):
    serializer_class = LibrarySerializer
    permission_classes = [permissions.IsAuthenticated]


class LibraryDelete(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request, pk: int, format=None) -> Response:
        entry = Library.objects.get(pk)

        if entry.user.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MarketList(generics.ListAPIView):
    serializer_class = MarketSerializer
    queryset = Market.objects.all()


class BuyListList(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, user_id: int, format=None):
        if user_id != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        buy_list = BuyList.objects.filter(user_id=user_id)
        serializer = BuyListSerializer(buy_list, many=True, context={'request': request})
        return Response(serializer.data)


class BuyListAdd(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BuyListSerializer


class HistoryList(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, user_id: int, format=None):
        if user_id != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        history = ReadHistory.objects.filter(user_id=user_id)
        serializer = HistorySerializer(history, many=True, context={'request': request})
        return Response(serializer.data)


class HistoryEntryAdd(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HistorySerializer


class HistoryEntryDelete(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request, pk: int, format=None) -> Response:
        entry = ReadHistory.objects.get(pk)

        if entry.user.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
