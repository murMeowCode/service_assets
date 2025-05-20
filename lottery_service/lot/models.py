from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Lottery(models.Model):
    title = models.CharField(max_length=120)
    end_date = models.DateTimeField(null=False)
    prize_fund = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    tickets_sold = models.PositiveIntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    prize_percent = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(70)]
    )
    base_fund = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title

class Participant(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('winner', 'Winner'),
        ('partial_winner', 'Partial Winner'),
        ('loser', 'Loser'),
    ]
    user_id = models.BigIntegerField()
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='waiting')
    prize_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Participant {self.user_id} in {self.lottery.title}"