from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ParseError
from django.shortcuts import get_object_or_404
from .models import Account, KeyChecker
from .crypto import encrypt_password, decrypt_password, check_masterkey, generate_key
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
        try:
            user_key = self.request.headers['User-Key']
            if KeyChecker.check_user_key(self.request.user, user_key):
                masterkey = KeyChecker.get_masterkey(
                    self.request.user, user_key)
                password = serializer.validated_data["password"]
                serializer.validated_data["password"] = encrypt_password(
                    password, masterkey)
                serializer.save(owner=self.request.user)
            else:
                raise ParseError(detail="User key is not valid")
        except KeyError:
            raise ParseError(
                detail="Request does not contain User-Key header.")

    def update(self, request, pk=None, *args, **kwargs):
        try:
            user_key = self.request.headers['User-Key']
            if KeyChecker.check_user_key(self.request.user, user_key):
                masterkey = KeyChecker.get_masterkey(self.request.user, user_key)
                super().update(request)
                account = Account.objects.get(id=pk)
                account.password = encrypt_password(request.data["password"], masterkey)
                account.save()
                serializer = AccountSerializer(account, context={"request": request})

                return Response(serializer.data)
            else:
                raise ParseError(detail="User key is not valid")
        except KeyError:
            raise ParseError(
                detail="Request does not contain User-Key header.")

    @action(detail=True, methods=["POST"])
    def decrypt_password(self, request, pk=None):
        try:
            user_key = self.request.headers['User-Key']
            if KeyChecker.check_user_key(self.request.user, user_key):
                masterkey = KeyChecker.get_masterkey(self.request.user, user_key)
                account = self.get_object()
                load = {
                    "plain_password": decrypt_password(account.password, masterkey),
                }
                return Response(load)
            else:
                raise ParseError(detail="User key is not valid")
        except KeyError:
            raise ParseError(
                detail="Request does not contain User-Key header.")

    @action(detail=True, methods=["POST"])
    def move_to_trash(self, request, pk=None):
        account = self.get_object()
        Account.move_to_trash(account.id, request.user)

        return Response()

    @action(detail=True, methods=["POST"])
    def restore_from_trash(self, request, pk=None):
        account = self.get_object()
        Account.restore(account.id, request.user)

        return Response()


@api_view(["POST"])
def search_account(request):
    queryset = Account.search_account(request.user, request.data["query"])
    serializer = AccountSerializer(
        queryset, many=True, context={"request": request})

    return Response(serializer.data)
