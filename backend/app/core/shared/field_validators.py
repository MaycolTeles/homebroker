"""
Module containing all custom field validators for model fields.
"""

from datetime import timedelta
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from core.shared.utils import aware_datetime_now


EIGHTEEN_YEARS_IN_DAYS = 18 * 365


class MinAgeValidator(MaxValueValidator):
    """
    Validates the birthdate belongs to an adult (i.e.: more than 18 years old).
    """

    message = _("Ensure age is greather than or equal to 18 years old.")
    code = "not_old_enough"

    def __init__(self, **kwargs) -> None:
        """
        Define the `min_birthdate` to be 18 years ago.
        """
        min_birthdate = aware_datetime_now() - timedelta(days=EIGHTEEN_YEARS_IN_DAYS)
        super().__init__(limit_value=min_birthdate, **kwargs)


class NonNegativeValueValidator(MinValueValidator):
    """
    Validates the amount is a non-negative number (i.e.: greather than or equal to zero).
    """

    def __init__(self, **kwargs) -> None:
        """
        Define the minimal value to be at least 0.0.
        """
        super().__init__(limit_value=Decimal(0.0), **kwargs)
