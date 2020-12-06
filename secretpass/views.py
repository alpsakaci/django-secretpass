from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from .models import Account
from .crypto import encrypt_password, decrypt_password
from .serializers import UserSerializer, AccountSerializer
from .permissions import IsOwner
import string
import random


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        super().update(request)
        user = User.objects.get(id=pk)
        user.set_password(request.data["password"])
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticated)

    def list(self, request):
        queryset = Account.get_user_accounts(request.user)
        serializer = AccountSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        account = self.get_object()
        serializer = AccountSerializer(account, context={"request": request})

        return Response(serializer.data)

    def perform_create(self, serializer):
        password = serializer.validated_data["password"]
        serializer.validated_data["password"] = encrypt_password(password)
        serializer.save(owner=self.request.user)

    def update(self, request, pk=None, *args, **kwargs):
        super().update(request, *args, **kwargs)
        account = self.get_object()
        account.password = encrypt_password(request.data["password"])
        account.save()
        serializer = AccountSerializer(account, context={"request": request})

        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def decrypt_password(self, request, pk=None):
        user = request.user
        account = self.get_object()
        load = {
            "status": status.HTTP_200_OK,
            "plain_password": decrypt_password(account.password),
        }

        return Response(load)


@api_view(["POST"])
def search_account(request):
    queryset = Account.search_account(request.user, request.data["query"])
    serializer = AccountSerializer(queryset, many=True, context={"request": request})

    return Response(serializer.data)
