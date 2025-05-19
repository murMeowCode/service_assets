# celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('lottery')

app.conf.beat_schedule = {
    'check-finished-lotteries': {
        'task': 'lot.tasks.check_finished_lotteries',
        'schedule': crontab(minute='*/1'), 
    },
}