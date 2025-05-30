"""
Module for providing the Celery app instance.

This will make sure the app is always imported when Django starts so that shared_task will use this app.
"""

__all__ = ("celery_app",)


from .celery import app as celery_app
