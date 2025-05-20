import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lottery_service.settings')

# Создаем экземпляр Celery
app = Celery('lottery_service')

# Загружаем конфигурацию из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоподгрузка задач из всех INSTALLED_APPS
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Регистрация периодических задач после инициализации"""
    # Импортируем модели ТОЛЬКО после полной загрузки Django
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    
    # Статическая задача (проверка лотерей каждую минуту)
    app.conf.beat_schedule = {
        'check-finished-lotteries-every-minute': {
            'task': 'lottery.tasks.check_and_process_finished_lotteries',
            'schedule': crontab(minute='*/1'),
        }
    }
    
    # Динамическая задача (создание лотерей)
    try:
        # Создаем или обновляем интервал
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=settings.TIME_LAG,
            period=IntervalSchedule.MINUTES,
        )
        
        # Создаем или обновляем задачу
        PeriodicTask.objects.update_or_create(
            name='create-new-lotteries',
            defaults={
                'interval': schedule,
                'task': 'lottery.tasks.create_new_lottery',
                'enabled': True,
            }
        )
    except Exception as e:
        print(f"Error setting up periodic tasks: {e}")

def update_celery_schedule(new_time_lag):
    """Функция для обновления расписания при изменении TIME_LAG"""
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    
    try:
        # Обновляем интервал
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=new_time_lag,
            period=IntervalSchedule.MINUTES,
        )
        
        # Обновляем задачу
        PeriodicTask.objects.filter(name='create-new-lotteries').update(
            interval=schedule
        )
    except Exception as e:
        print(f"Error updating schedule: {e}")