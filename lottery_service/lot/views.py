from rest_framework import generics, permissions
from .models import Lottery, Participant
from .serializers import LotterySerializer, ParticipantSerializer
from rest_framework.response import Response
from django.utils import timezone
from .services.rabbitmq_service import RabbitMQService

class LotteryListAPIView(generics.ListAPIView):
    queryset = Lottery.objects.all()
    serializer_class = LotterySerializer

class ParticipantListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Participant.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        lottery_id = self.request.data.get('lottery_id')
        lottery = Lottery.objects.get(id=lottery_id)
        RabbitMQService.send_balance_update(self.request.user.id,lottery.ticket_price,"outcome")
        # Generate ticket number (you might want to implement a better logic)
        ticket_number = self.request.data.get('ticket')
        
        serializer.save(
            user_id=self.request.user.id,
            ticket_number=ticket_number,
            status='waiting',
            prize_amount=0
        )
        
        # Update tickets sold count
        lottery.tickets_sold += 1
        lottery.prize_fund = lottery.base_fund + lottery.tickets_sold * lottery.prize_percent
        lottery.save()