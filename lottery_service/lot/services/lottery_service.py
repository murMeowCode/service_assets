from lot.models import Lottery, Participant
from rabbitmq_service import RabbitMQService

class LotteryService:
    @staticmethod
    def process_finished_lotteries():
        from django.utils import timezone
        finished_lotteries = Lottery.objects.filter(
            is_finished=False,
            end_date__lte=timezone.now()
        )

        for lottery in finished_lotteries:
            LotteryService._process_lottery(lottery)

    @staticmethod
    def _process_lottery(lottery):
        participants = Participant.objects.filter(lottery_id=lottery.id)
        winners = LotteryService._select_winners(participants, lottery)
        
        for participant in participants:
            participant.status, participant.prize_amount = LotteryService._determine_prize(participant, winners)
            participant.save()
            
            if participant.prize_amount > 0:
                RabbitMQService.send_balance_update(
                    participant.user_id,
                    participant.prize_amount,
                    participant.prize_amount * 0.01
                )
            
            RabbitMQService.send_notification(participant)
        
        lottery.is_finished = True
        lottery.save()

    @staticmethod
    def _select_winners(participants, lottery):
        # Здесь должна быть ваша реальная логика выбора победителей
        # Это примерная реализация
        full_winners = {}
        partial_winners = {}
        
        if participants:
            full_winners[participants[0]] = lottery.prize_fund * 0.7
        if len(participants) > 1:
            partial_winners[participants[1]] = lottery.prize_fund * 0.2
        if len(participants) > 2:
            partial_winners[participants[2]] = lottery.prize_fund * 0.1
            
        return {
            'full_winners': full_winners,
            'partial_winners': partial_winners
        }

    @staticmethod
    def _determine_prize(participant, winners):
        if participant in winners['full_winners']:
            return 'winner', winners['full_winners'][participant]
        elif participant in winners['partial_winners']:
            return 'partial_winner', winners['partial_winners'][participant]
        return 'loser', 0