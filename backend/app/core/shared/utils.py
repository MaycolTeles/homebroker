"""
Module containing some utility functions.
"""

from datetime import datetime

from django.utils.timezone import get_current_timezone


def aware_datetime_now() -> datetime:
    """
    Return a datetime.now() object with tz info (aware).

    This function works the same as `aware_datetime`, but it doesn't get any
    date specification as it generates the date by using datetime.now()

    :return `datetime`: The datetime object created and made aware.
    """
    return datetime.now(tz=get_current_timezone())


def aware_datetime(**kwargs) -> datetime:
    """
    Make a datetime object aware.

    This function creates a datetime object and makes it aware
    by setting the timezone to the current timezone got by django.

    This ensures that all datetime objects are timezone-aware,
    thus this function should be used to create all datetime objects.

    Args:
        year (`int`): The year of the datetime object.
        month (`int`): The month of the datetime object.
        day (`int`): The day of the datetime object.
        hour (`int`): The hour of the datetime object. Default is 0.
        minute (`int`): The minute of the datetime object. Default is 0.
        second (`int`): The second of the datetime object. Default is 0.
        microsecond (`int`): The microsecond of the datetime object. Default is 0.

    Returns:
        `datetime`: The datetime object created and made aware.
    """
    return datetime(**kwargs, tzinfo=get_current_timezone())
