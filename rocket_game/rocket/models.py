from django.db import models

class GameAccount(models.Model):
    user_id = models.PositiveBigIntegerField()
    spins_least = models.SmallIntegerField(default=3)
    spin_cost = models.IntegerField(default=10)
    spin_coef = models.FloatField(default=1)
    life_upgrade_coef = models.FloatField(default=0)
    oil_upgrade_coef = models.FloatField(default=0)
    ammo_upgrade_coef = models.FloatField(default=0)
