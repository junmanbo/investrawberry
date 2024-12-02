from celery import Celery

# RabbitMQ connection URL
# Format: 'amqp://username:password@hostname:port/virtual_host'
BROKER_URL = "amqp://guest:guest@localhost:5672//"

# Create Celery app
app = Celery("tasks", broker=BROKER_URL, backend="redis://localhost:6379/1")

# Optional configurations
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True,
)
