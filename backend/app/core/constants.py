"""
Module containing some constants for the django orm database and other settings.
"""

from decouple import config


def _split_env_string(env_string: str) -> list[str]:
    """
    Parse a string from the environment into a list.

    Example:
    `"localhost 127.0.0.1 0.0.0.0"` -> [`"localhost"`, `"127.0.0.1"`, `"0.0.0.0"`]

    Args:
        env_string (`str`): The string to be parsed.
    """
    return env_string.split(" ")


DB: str = config("DB")  # type: ignore

DB_HOST: str = config("DB_HOST")  # type: ignore

DB_USER: str = config("DB_USER")  # type: ignore

DB_PASSWORD: str = config("DB_PASSWORD")  # type: ignore

DB_PORT: int = config("DB_PORT")

DB_NAME: str = config("DB_NAME")  # type: ignore

DJANGO_SECRET_KEY: str = config("DJANGO_SECRET_KEY")  # type: ignore

DJANGO_DEBUG: bool = config("DJANGO_DEBUG", cast=bool, default=False)

DJANGO_ALLOWED_HOSTS: list[str] = config("DJANGO_ALLOWED_HOSTS", cast=_split_env_string)  # type: ignore

DJANGO_CSRF_TRUSTED_ORIGINS: list[str] = config("DJANGO_CSRF_TRUSTED_ORIGINS", cast=_split_env_string)  # type: ignore

REDIS_HOST: str = config("REDIS_HOST")  # type: ignore

KAFKA_HOST: str = config("KAFKA_HOST")  # type: ignore
