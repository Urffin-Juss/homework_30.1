import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_app.settings")

app = Celery("celery_app")

app.config_from_object("celery_app.settings")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-inactive-users': {
        'task': 'users.tasks.check_inactive_users',
        'schedule': crontab(hour=3, minute=0),  # Ежедневно в 3:00
    },
    'check-course-updates': {
        'task': 'courses.tasks.check_and_send_updates',
        'schedule': crontab(minute='*/30'),  # Каждые 30 минут
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')