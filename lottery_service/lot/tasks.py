from celery import shared_task
from .services.lottery_service import LotteryService
from .models import Lottery
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

@shared_task(name="lot.tasks.check_and_process_finished_lotteries")
def check_and_process_finished_lotteries():
    LotteryService.process_finished_lotteries()
    
@shared_task(name="lot.tasks.create_new_lottery")
def create_new_lottery():
    # Получаем все незавершенные лотереи
    active_lotteries = Lottery.objects.filter(is_finished=False).order_by('-end_date')
    
    # Если активных лотерей меньше 4
    if active_lotteries.count() < 4:
        # Берем самую позднюю дату окончания или текущее время, если лотерей нет
        latest_end_date = active_lotteries.first().end_date if active_lotteries.exists() else timezone.now()
        
        # Создаем новую лотерею с end_date +15 минут от самой поздней
        new_end_date = latest_end_date + timedelta(minutes=settings.TIME_LAG)
        
        Lottery.objects.create(
            end_date=new_end_date,
            is_finished=False,
            ticket_price = 100,
            tickets_sold = 0,
            prize_fund=10000,
            base_fund = 5000,
            prize_percent = 50,
            title = 'Быстрая лотерея'

        )
        return f"Created new lottery ending at {new_end_date}"
    
    return "No new lottery needed - already have 4 or more active"