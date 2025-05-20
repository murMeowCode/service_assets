from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User

@receiver(pre_save, sender=User)
def update_vip_level(sender, instance, **kwargs):
    """
    Автоматически обновляет VIP-уровень пользователя при изменении баланса
    """
    if instance.pk:  # Проверяем, что это обновление существующего пользователя
        try:
            old_user = User.objects.get(pk=instance.pk)
            
            # Если баланс изменился
            if old_user.balance != instance.balance:
                # Определяем новый VIP-уровень
                if instance.balance >= 50000:
                    new_level = 3
                elif instance.balance >= 10000:
                    new_level = 2
                elif instance.balance >= 5000:
                    new_level = 1
                else:
                    new_level = 0
                
                # Обновляем только если уровень изменился
                if instance.vip_level != new_level:
                    instance.vip_level = new_level
                    
        except User.DoesNotExist:
            pass  # Пользователь не существует, пропускаем