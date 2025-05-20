from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction



class User(AbstractUser):
    balance = models.FloatField()
    balance_virtual = models.FloatField()
    birthday = models.DateField(null=True)
    father_name = models.CharField(max_length=25,null=True,verbose_name='Отчество')
    vip_level = models.BigIntegerField(default=0) 
    is_root = models.BooleanField(default=False)
    
@receiver(pre_save, sender=User)
def update_vip_level(sender, instance, **kwargs):
    if instance.pk:  # Проверяем, что это обновление существующего пользователя
        old_user = User.objects.get(pk=instance.pk)
        if old_user.balance != instance.balance:  # Если баланс изменился
            # Определяем новый VIP-уровень на основе баланса
            if instance.balance >= 50000:
                instance.vip_level = 3
            elif instance.balance >= 10000:
                instance.vip_level = 2
            elif instance.balance >= 5000:
                instance.vip_level = 1
            else:
                instance.vip_level = 0