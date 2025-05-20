import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lottery_service.settings')

app = Celery('lottery_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Явно указываем использовать DatabaseScheduler
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Инициализация периодических задач"""
    update_celery_intervals()  # Теперь интервал всегда актуален
    
    from django_celery_beat.models import (PeriodicTask, 
                                         IntervalSchedule,
                                         CrontabSchedule)
    
    try:
        # 1. Задача для создания новых лотерей (по интервалу)
        interval, _ = IntervalSchedule.objects.get_or_create(
            every=settings.TIME_LAG,
            period=IntervalSchedule.MINUTES,
        )
        
        PeriodicTask.objects.update_or_create(
            name='create-new-lotteries',
            defaults={
                'interval': interval,
                'task': 'lot.tasks.create_new_lottery',
                'enabled': True,
            }
        )
        
        # 2. Задача для проверки завершенных лотерей (по crontab)
        cron, _ = CrontabSchedule.objects.get_or_create(
            minute='*/1',
            hour='*',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone=settings.TIME_ZONE
        )
        
        PeriodicTask.objects.update_or_create(
            name='check-finished-lotteries',
            defaults={
                'crontab': cron,  # Передаем объект, а не словарь
                'task': 'lot.tasks.check_and_process_finished_lotteries',
                'enabled': True,
            }
        )
        
        print("Successfully setup periodic tasks")
    except Exception as e:
        print(f"Error setting up periodic tasks: {e}")
        
def update_celery_intervals():
    """Обновляет интервалы задач при изменении TIME_LAG"""
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    
    try:
        # Получаем или создаем новый интервал
        new_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=settings.TIME_LAG,
            period=IntervalSchedule.MINUTES,
        )
        
        # Обновляем задачу
        PeriodicTask.objects.filter(
            name='create-new-lotteries'
        ).update(interval=new_schedule)
        
        print(f"Updated interval to {settings.TIME_LAG} minutes")
    except Exception as e:
        print(f"Error updating intervals: {e}")