"""
Base test case for all test cases in the project.

This module defines a `BaseTestCase` class that provides common functionality
for all the non-API test cases in the project.

For API test cases, use the `BaseAPITestCase` class in the `base_api_test_case.py` module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import TestCase, TransactionTestCase


if TYPE_CHECKING:
    from account.models import User


class _CreateUserMixin:
    """
    Mixin to create a user instance.

    This mixin provides a method to create a user instance using the `mixer` library.
    """

    def create_user(self, **kwargs) -> User:
        """
        Create a user instance.

        This method creates a user instance using the `mixer` library.
        Additional arguments and keyword arguments can be passed to the method to customize the user instance.
        """
        # Importing mixer here to avoid needing to add it as a production dependency.
        from mixer.backend.django import mixer

        from account.models import User

        user: User = mixer.blend(User, **kwargs)  # type: ignore
        return user


class BaseTestCase(TestCase, _CreateUserMixin):
    """
    Base Test Case class containing common methods for all test cases.
    """


class BaseTransactionTestCase(TransactionTestCase, _CreateUserMixin):
    """
    Base Transaction Test Case class containing common methods for all test cases.
    """
