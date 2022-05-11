from rest_framework import serializers

from ..models import User, Comment, ReadHistory, BuyList, Market, Library


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'coins', 'is_creator']
        # fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadHistory
        fields = '__all__'


class BuyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyList
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
