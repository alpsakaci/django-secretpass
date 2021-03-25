from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ParseError
from django.shortcuts import get_object_or_404
from .models import Account
from .serializers import UserSerializer, AccountSerializer
from .permissions import IsOwner
import string
import random
from secretpass.account_selector import get_account_by_id, get_accounts_by_user, get_accounts_in_trash, search_accounts
from secretpass.account_service import create_account, update_account, decrypt_account_password, move_to_trash, restore
from secretpass.profile_service import check_master_password, create_profile


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
        accounts = get_accounts_by_user(request.user)
        serializer = AccountSerializer(
            accounts, many=True, context={"request": request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        account = self.get_object()
        serializer = AccountSerializer(account, context={"request": request})

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            master_password = self.request.headers['Master-Password']
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            service = serializer.validated_data["service"]
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            account = create_account(
                self.request.user, service, username, password, master_password)
            serializer = AccountSerializer(account)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            raise ParseError(
                detail="Request does not contain Master-Password header.")
        except ParseError as e:
            raise e

    def update(self, request, pk=None, *args, **kwargs):
        try:
            master_password = self.request.headers['Master-Password']
            account = self.get_object()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            service = serializer.validated_data["service"]
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            account = update_account(
                account, service, username, password, master_password)
            serializer = AccountSerializer(
                account, context={"request": request})

            return Response(serializer.data)
        except KeyError:
            raise ParseError(
                detail="Request does not contain Master-Password header.")
        except ParseError as e:
            raise e

    @action(detail=True, methods=["POST"])
    def decrypt_password(self, request, pk=None):
        try:
            master_password = self.request.headers['Master-Password']
            account = self.get_object()
            load = {
                "plain_password": decrypt_account_password(account, master_password)
            }
            return Response(load)
        except KeyError:
            raise ParseError(
                detail="Request does not contain Master-Password header.")
        except ParseError as e:
            raise e

    @action(detail=True, methods=["POST"])
    def move_to_trash(self, request, pk=None):
        account = self.get_object()
        move_to_trash(account)

        return Response({'message': 'Account moved to trash.'})

    @action(detail=True, methods=["POST"])
    def restore_from_trash(self, request, pk=None):
        account = self.get_object()
        restore(account)

        return Response({'message': 'Account restored from trash.'})


@api_view(["POST"])
def verify_master_password(request):
    master_password = request.data["master_password"]
    try:
        check_master_password(
            master_password, request.user.profile.salt, request.user.profile.master_password)
        return Response({'message': 'Master Password is valid.'})
    except ParseError as e:
        raise e


@api_view(["POST"])
def create_user_profile(request):
    master_password = request.data["master_password"]
    try:
        create_profile(request.user, master_password)
        return Response({'message': 'Profile created.'})
    except ValidationError as e:
        raise ParseError(detail="Profile with this user already exists.")


@api_view(["POST"])
def search_account(request):
    queryset = search_accounts(request.user, request.data["query"])
    serializer = AccountSerializer(
        queryset, many=True, context={"request": request})

    return Response(serializer.data)
