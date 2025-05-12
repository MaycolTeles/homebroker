"""
Base ViewSet class to be used by all other ViewSets in the app.
"""

from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    """
    Base ViewSet class to be used by other ViewSets in the app.

    This ViewSet class must be inherited by all other ViewSets in the app
    that needs the common behavior of filtering the queryset based on the user.

    This class provides a common `get_queryset` method that filters the queryset based on the user.
    If the user is a superuser, the entire queryset is returned.

    Inheriting this class ensures that the queryset is filtered based on the user. If you don't want this behavior,
    inherit from `ModelViewSet` directly.

    Methods:
        `get_queryset`: Method to get the queryset based on the user.
    """

    queryset: QuerySet

    def get_queryset(self) -> QuerySet:
        """
        Get the queryset based on the user.

        This method filters the queryset based on the user.
        If the user is a superuser, the entire queryset is returned.

        Returns:
            `QuerySet`: The filtered queryset based on the user.
        """
        from account.models import User

        user: User = self.request.user  # type: ignore

        if user.is_superuser:
            return self.queryset.all()

        return self.queryset.filter(user=user)
