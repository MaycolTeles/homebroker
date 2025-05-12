"""
Module containing all the URL patterns for the Account app.
"""

from rest_framework import routers

from account.views import AccountViewSet, AuthViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"users", UserViewSet, basename="users")
