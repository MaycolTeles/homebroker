"""
Module containing the Auth serializers.
"""

from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from account.exceptions import UserAlreadyExistsException
from account.models import User


class LoginSerializer(serializers.Serializer):
    """
    Class to serializer the login user method.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the data to log the user in.

        Args:
            data (`dict[str, Any]`): The data to log the user in (username and password).

        Returns:
            `dict[str, Any]`: A dict containing the user.

        Raises:
            `ValidationError`: If the username or password is missing.
            `AuthenticationFailed`: If the credentials are incorrect.
        """
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            msg = "Both username and password are required."
            raise serializers.ValidationError(msg)

        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed

        data["user"] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Class to serialize the register user method.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "birthdate",
            "password",
        )

    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data: dict[str, Any]) -> User:
        """
        Create a new user instance.

        Args:
            validated_data (`dict[str, Any]`): All necessary data (already validated) to create a new user.

        Returns:
            `User`: The new user instance.
        """
        email = validated_data["email"]

        user = User.objects.create_user(
            email=email,
            username=validated_data.get("username", email),
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            birthdate=validated_data["birthdate"],
            password=validated_data["password"],
        )
        return user

    def validate_email(self, email: str) -> str:
        """
        Validate if the email is unique.

        Raise an exception if there's an user with that email already.

        Args:
            email (`str`): The email to be validated.

        Returns:
            `str`: The email if it's valid.

        Raises:
            `UserAlreadyExistsException`: If there's an user with that email already.
        """
        if User.objects.filter(email=email).exists():
            raise UserAlreadyExistsException

        return email
