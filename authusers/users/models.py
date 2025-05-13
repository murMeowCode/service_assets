from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    role = models.IntegerField()
    birthday = models.DateField(null=True)
    father_name = models.CharField(max_length=25,null=True,verbose_name='Отчество') 