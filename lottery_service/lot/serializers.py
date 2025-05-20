from rest_framework import serializers
from .models import Lottery, Participant

class LotterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lottery
        fields = '__all__'
        read_only_fields = ('tickets_sold', 'is_finished')
        
class TimeLagSerializer(serializers.Serializer):
    time_lag = serializers.IntegerField(
        required=True,
        min_value=10,
        max_value=30,
        help_text="Time lag in minutes"
    )

class ParticipantSerializer(serializers.ModelSerializer):
    lottery_title = serializers.CharField(source='lottery.title', read_only=True)
    lottery_id = serializers.IntegerField(write_only=True)  # Добавляем явное поле для записи
    
    class Meta:
        model = Participant
        fields = '__all__'
        read_only_fields = ('user_id', 'ticket_number', 'status', 'prize_amount', 'lottery')  # Добавляем lottery в read_only