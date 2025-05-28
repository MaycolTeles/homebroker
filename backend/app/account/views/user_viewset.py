"""
Module containing the User views.
"""

from rest_framework.viewsets import ModelViewSet

from account.models import User
from account.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    API endpoint to define User actions.

    The available actions for the User model are:
    * List
    * Create
    * Retrieve
    * Update
    * Partial Update
    * Destroy
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
