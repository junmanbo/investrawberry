from celery.result import AsyncResult
from celery import Celery
import os


RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
RABBITMQ_HOSTNAME = os.getenv("RABBITMQ_HOSTNAME", "localhost")

REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")

broker_url = (
    f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOSTNAME}:5672//"
)
backend_url = f"redis://{REDIS_HOSTNAME}:6379/0"

celery_app = Celery("worker", broker=broker_url, backend=backend_url)
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
