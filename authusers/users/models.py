from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    balance_virtual = models.DecimalField(max_digits=10, decimal_places=2)
    birthday = models.DateField(null=True)
    father_name = models.CharField(max_length=25,null=True,verbose_name='Отчество') 