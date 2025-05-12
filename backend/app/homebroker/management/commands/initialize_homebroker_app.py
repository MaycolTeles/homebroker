"""
Module containing the `initialize_homebroker_app` command.
"""

import djclick as click

from core.logger import get_logger
from homebroker.tasks import (
    task_create_default_assets,
    task_create_default_assets_dailies,
)


logger = get_logger(component="homebroker", subcomponent="commands", command="initialize_homebroker_app")


@click.command()
def initialize_homebroker_app() -> None:
    """
    Initialize the Homebroker app.

    This command initializes the homebroker app up by
        1. Creating all default assets instances;
        2. Creating all default assets dailies instances.

    To execute this command, run the following command:

    .. code-block:: bash
        $ python manage.py setup_homebroker
    """
    logger.info("Initializing Homebroker App.")

    try:
        task_create_default_assets.delay()
        task_create_default_assets_dailies.delay()

    except Exception:
        logger.exception("An error occurred while initializing Homebroker app.")
