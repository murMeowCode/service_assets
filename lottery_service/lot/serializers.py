from rest_framework import serializers
from .models import Lottery, Participant

class LotterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lottery
        fields = '__all__'
        read_only_fields = ('tickets_sold', 'is_finished')

class ParticipantSerializer(serializers.ModelSerializer):
    lottery_title = serializers.CharField(source='lottery.title', read_only=True)
    
    class Meta:
        model = Participant
        fields = '__all__'
        read_only_fields = ('user_id', 'ticket_number', 'status', 'prize_amount')