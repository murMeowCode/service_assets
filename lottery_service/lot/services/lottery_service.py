from pygost import gost28147
import secrets
from lot.models import Lottery, Participant
from .rabbitmq_service import RabbitMQService

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
    def _generate(number):
        '''
        Функция генерации случайного числа из числа сочетаний
        number: количество сочетаний
        '''
        key = secrets.token_bytes(32)
        sbox = "id-Gost28147-89-CryptoPro-A-ParamSet"
        random_bytes = gost28147.encrypt(key=key,ns= (1,1), sbox = sbox)
        PSP = random_bytes[1]
        result = (PSP % number) + 1
        
        return result

    
    @staticmethod
    def _process_lottery(lottery):
        participants = Participant.objects.filter(lottery_id=lottery.id)
        winners = LotteryService._select_winners(participants)
        
        for participant in participants:
            participant.status, participant.prize_amount = LotteryService._determine_prize(participant, winners,lottery)
            participant.save()
            
            if participant.prize_amount > 0:
                RabbitMQService.send_balance_update(
                    participant.user_id,
                    participant.prize_amount,
                    "income",
                    "real"
                )
            
            RabbitMQService.send_notification(participant)
        
        lottery.is_finished = True
        lottery.save()

    @staticmethod
    def _select_winners(participants, lottery):
        
        win = list()
        for _ in range(4):
            win.append(LotteryService._generate(3))
        
        full_winners = []
        partial_winners = []

        for participant in participants:
            # Преобразуем строку '1234' в [1, 2, 3, 4]
            ticket_numbers = [int(digit) for digit in participant.ticket]
            
            match_count = 0
            for i in range(4):
                if ticket_numbers[i] == win[i]:
                    match_count += 1
                else:
                    break  # Прерываем, если не совпадает очередное число
            
            if match_count == 4:
                full_winners.append(participant)
            elif match_count == 3:
                partial_winners.append(participant)
            
        return {
            'full_winners': full_winners,
            'partial_winners': partial_winners
        }

    @staticmethod
    def _determine_prize(participant, winners, lottery):
        if participant in winners['full_winners']:
            return 'winner', (lottery.prize_fund - len(winners['partial_winners']) * lottery.ticket_price * 2)/len(winners['full_winners'])
        elif participant in winners['partial_winners']:
            return 'partial_winner', lottery.ticket_price * 2
        return 'loser', 0