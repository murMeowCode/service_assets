from django.db import models

class Lottery(models.Model):
    title = models.CharField(max_length=120)
    end_date = models.DateTimeField(null=False)
    prize_fund = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)  # New field
    tickets_sold = models.PositiveIntegerField(default=0)  # New field
    is_finished = models.BooleanField(default=False)
    prize_percent = models.IntegerField(range(50,70))
    base_fund = models.DecimalField()
    
    def __str__(self):
        return self.title
    
class Participant(models.Model):
    user_id = models.UUIDField()
    lottery_id = models.ForeignKey(Lottery)
    ticket_number = models.CharField()
    status = models.CharField(default='waiting')
    prize_amount = models.DecimalField()