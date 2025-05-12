"""
Module containing the tests for the Auth ViewSet.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from core.mixins import BaseAPITestCase
from core.shared import aware_datetime


class AuthViewSetTestCase(BaseAPITestCase):
    """
    Test case for the Auth ViewSet.
    """

    def test_should_register_user(self):
        """
        Assert the viewset register a new user by creating a token for them.
        """
        test_first_name = "test_first_name"
        test_last_name = "test_last_name"
        test_email = "test_email@email.com"
        test_birthdate = aware_datetime(day=14, month=10, year=2000)
        test_password = "test_password"  # noqa: S105 (Possible hardcoded password)

        data = {
            "first_name": test_first_name,
            "last_name": test_last_name,
            "email": test_email,
            "birthdate": test_birthdate,
            "password": test_password,
        }
        url = reverse("auth-register")
        response = self.client.post(url, data)
        r = response.json()
        user_id = r["user"]["id"]
        token = r["token"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(token, Token.objects.get(user_id=user_id).key)

    def test_should_not_register_user_when_missing_required_field(self):
        """
        Assert the viewset does not register a new user.

        Assert the viewset returns an error (HTTP_422_UNPROCESSABLE_ENTITY) instead
        when a required field is missing in the request.
        """
        test_first_name = "test_first_name"
        test_last_name = "test_last_name"
        test_email = "test_email@email.com"
        test_password = "test_password"  # noqa: S105 (Possible hardcoded password)

        # Missing birthdate
        data = {
            "username": test_email,
            "first_name": test_first_name,
            "last_name": test_last_name,
            "email": test_email,
            "password": test_password,
        }

        url = reverse("auth-register")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Token.objects.count(), 0)

    def test_should_not_regiser_user_twice(self):
        """
        Assert the viewset does not register a new user twice.
        """
        test_first_name = "test_first_name"
        test_last_name = "test_last_name"
        test_email = "test_email@email.com"
        test_birthdate = aware_datetime(day=14, month=10, year=2000)
        test_password = "test_password"  # noqa: S105 (Possible hardcoded password)

        data = {
            "username": test_email,
            "first_name": test_first_name,
            "last_name": test_last_name,
            "email": test_email,
            "birthdate": test_birthdate,
            "password": test_password,
        }

        url = reverse("auth-register")

        # First call, should be OK
        self.client.post(url, data)

        # Calling it again, should return an error
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Token.objects.count(), 1)  # Only a single token was created (the first time)

    def test_should_log_user_in(self):
        """
        Assert the viewset log a user in.
        """
        test_username = self.user.username
        test_password = "test_password"  # noqa: S105 (Possible hardcoded password)

        self.user.set_password(test_password)
        self.user.save(update_fields=("password",))

        data = {
            "username": test_username,
            "password": test_password,
        }
        url = reverse("auth-login")
        response = self.client.post(url, data)
        r = response.json()
        user_id = r["user"]["id"]
        token = r["token"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_authenticated)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(token, Token.objects.get(user_id=user_id).key)

    def test_should_not_log_user_in_when_missing_required_fields(self):
        """
        Assert the viewset does not log an user in.

        Assert the viewset returns an error (HTTP_400_BAD_REQUEST) instead
        when a required field is missing in the request.
        """
        test_username = "test_first_name"

        # Missing password
        data = {
            "username": test_username,
        }

        url = reverse("auth-login")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Token.objects.count(), 0)

    def test_should_not_log_user_in_when_credentials_are_incorrect(self):
        """
        Assert the viewset does not log an user in.

        Assert the viewset returns an error response (HTTP_401_UNAUTHORIZED) instead
        when the credentials are incorrect.
        """
        test_username = "test_first_name"
        test_password = "test_wrong_password"  # noqa: S105 (possible hardcoded password)

        # Missing password
        data = {"username": test_username, "password": test_password}

        url = reverse("auth-login")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Token.objects.count(), 0)

    def test_should_log_user_out(self):
        """
        Assert the viewset log a user out.
        """
        Token.objects.create(user=self.user)
        self.login()

        url = reverse("auth-logout")
        response = self.client.post(url)

        # Asserting that the response is OK
        # The user is no longer authenticated
        # And the Token was deleted
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user_id=self.user.id).exists())
