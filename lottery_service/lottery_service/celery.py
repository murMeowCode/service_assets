import os
from celery import Celery
from celery.schedules import crontab

# 1. Устанавливаем переменную окружения ДО создания экземпляра Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lottery_service.settings')

# 2. Создаем экземпляр Celery
app = Celery('lottery_service')

# 3. Загружаем конфигурацию из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Откладываем импорт задач до полной загрузки Django
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Регистрация периодических задач после инициализации"""
    app.conf.beat_schedule = {
    'check-finished-lotteries-every-minute': {
        'task': 'check_and_process_finished_lotteries',
        'schedule': crontab(minute='*/1'),
    },
}

# 5. Автоподгрузка задач из всех INSTALLED_APPS
app.autodiscover_tasks()