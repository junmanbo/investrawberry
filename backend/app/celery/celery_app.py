from celery.schedules import crontab
from .celery_config import app

app.conf.beat_schedule = {
    # Run at specific times using crontab
    "daily-at-midnight": {
        "task": "tasks.rebalancing_task",
        "schedule": crontab(hour=0, minute=0),
    },
    "daily-at-midnight": {
        "task": "tasks.rebalancing_task",
        "schedule": crontab(hour=0, minute=0),
    },
    # # Run every hour
    # "hourly-task": {
    #     "task": "tasks.rebalancing_task",
    #     "schedule": crontab(minute=0),
    # },
    # # Run every weekday morning at 7:30
    # "weekday-morning": {
    #     "task": "tasks.rebalancing_task",
    #     "schedule": crontab(hour=7, minute=30, day_of_week="1-5"),
    # },
}
