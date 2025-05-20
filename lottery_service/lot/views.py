from rest_framework import generics, permissions, viewsets, mixins
from lottery_service.celery import update_celery_intervals
from .models import Lottery, Participant
from .serializers import LotterySerializer, ParticipantSerializer, TimeLagSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework import status
from .services.rabbitmq_service import RabbitMQService
from django.db.models import Sum, Count
from django.db import models
from rest_framework.permissions import AllowAny, IsAuthenticated

class LotteryViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin):
    queryset = Lottery.objects.all()
    serializer_class = LotterySerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]  # Разрешить всем
        else:
            permission_classes = [IsAuthenticated]  # Требовать авторизацию для остальных действий
        return [permission() for permission in permission_classes]

class TimeLagAPIView(APIView):
    """
    API для получения и обновления параметра time_lag
    """
    def get(self, request):
        # Получаем текущее значение time_lag из настроек
        data = {
            'time_lag': getattr(settings, 'TIME_LAG', 0)
        }
        return Response(data)

    def patch(self, request):
        serializer = TimeLagSerializer(data=request.data)
        if serializer.is_valid():
            new_time_lag = serializer.validated_data['time_lag']
            setattr(settings, 'TIME_LAG', new_time_lag)
            update_celery_intervals()   # Обновляем расписание
            return Response({'time_lag': new_time_lag})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParticipantListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Participant.objects.filter(user_id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Основные данные
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Агрегированные данные
        aggregates = queryset.aggregate(
            total_count=Count('id'),
            total_prize=Sum('prize_amount'),
            winner_count=Count('id', filter=models.Q(status='winner')),
            partial_winner_count=Count('id', filter=models.Q(status='partial_winner')))
        
        # Статусная статистика
        status_stats = dict(
            queryset.values_list('status')
                  .annotate(count=Count('status')))
        
        response_data = {
            'participants': data,
            'stats': {
                'total_count': aggregates['total_count'],
                'total_prize_amount': aggregates['total_prize'] or 0,
                'status_counts': {
                    'winner': aggregates['winner_count'],
                    'partial_winner': aggregates['partial_winner_count'],
                },
                'detailed_status_stats': status_stats,
            }
        }
        
        return Response(response_data)
    
    def perform_create(self, serializer):
        lottery = self.request.data.get('lottery_id')
        lottery = Lottery.objects.get(id=lottery)
        RabbitMQService.send_balance_update(self.request.user.id,lottery.ticket_price,"outcome",self.request.data["value_type"])
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