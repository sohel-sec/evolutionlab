# celery_schedule.py

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'schedule_task.tasks.add': {
        'task': 'schedule_task.tasks.add',
        'schedule': 3  # Schedule the task daily at midnight
    },
   
}
