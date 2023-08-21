from celery.result import AsyncResult
from celery import Celery

# celery_app = Celery("worker", broker="amqp://guest@queue//")
celery_app = Celery(
    "worker", broker="amqp://guest@localhost:5672//", backend="redis://localhost:6379/0"
)
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.task_routes = {
    "app.worker.place_order": "order",
    "app.worker.portfolio_order": "order",
}


def get_task_info(task_id):
    """
    task_id에 따른 task 정보를 반환
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result
