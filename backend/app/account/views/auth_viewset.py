"""
Module containing the API Auth views.
"""

import random

from django.contrib.auth import login, logout
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from account.models import Account, User
from account.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from core.logger import get_logger


logger = get_logger(component="account", subcomponent="views", viewset="AuthViewSet")


class AuthViewSet(viewsets.ViewSet):
    """
    API endpoints to handle user authentication.
    """

    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=("post",), url_path="register", url_name="register")
    def register(self, request: Request) -> Response:
        """
        Register a new user in the app.

        The registration process occurs in the following order:
            1. Creates a new user;
            2. Creates a new token for that new user;
            3. Returns the user data and the token.
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()

        _create_account(user)

        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "user": user_data,
            "token": token.key,
        }
        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=("post",), url_path="login", url_name="login")
    def login(self, request: Request) -> Response:
        """
        Log the user in.

        The login process occurs in the following order:
            1. Validates the user credentials;
            2. Log the user in;
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = serializer.validated_data["user"]  # type: ignore
        login(request, user)  # type: ignore

        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "user": user_data,
            "token": token.key,
        }
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=("post",), url_path="logout", url_name="logout")
    def logout(self, request: Request) -> Response:
        """
        Log the user out.

        The logout process occurs in the following order:
            1. Deletes the user auth token;
        """
        request.user.auth_token.delete()
        logout(request)  # type: ignore

        response = {"message": "User logged out successfully"}
        return Response(response, status=status.HTTP_200_OK)


def _create_account(user: User) -> None:
    """
    Create an account for the user.
    """
    bank = random.choice(["001", "033", "104", "237", "341"])  # noqa: S311
    agency = f"{random.randint(1000, 9999)}-{random.randint(0, 9)}"  # noqa: S311
    account_number = f"{''.join(str(random.randint(0, 9)) for _ in range(8))}-{random.randint(0, 9)}"  # noqa: S311
    Account.objects.create(user=user, bank=bank, agency=agency, account_number=account_number)
