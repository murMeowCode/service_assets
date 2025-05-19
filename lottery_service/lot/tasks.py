from celery import shared_task
from .services.lottery_service import LotteryService

@shared_task(name="check_and_process_finished_lotteries")
def check_and_process_finished_lotteries():
    LotteryService.process_finished_lotteries()