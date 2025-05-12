"""
Module containing the `task_process_order` task.
"""

from celery import shared_task

from core.logger import get_logger


logger = get_logger(component="homebroker", subcomponent="tasks", task="task_process_order")


@shared_task
def task_process_order(order_id: str) -> None:
    """
    Process an order.

    To process an order, the order needs to be executed.
    See more details in `OrderService().execute_order(order)` docs.

    Args:
        order_id (`str`): The id of the order to be processed.
    """
    from homebroker.models import Order
    from homebroker.services import OrderService

    logger.info('task "task_process_order" started.')

    order: Order = Order.objects.get(id=order_id)
    OrderService().execute_order(order)

    logger.info('task "task_process_order" finished.')
