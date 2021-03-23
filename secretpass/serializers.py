from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    date_joined = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "date_joined",
            "is_active",
        ]


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    service = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
