from django.db import models

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)  # Автоинкрементный ID
    role_literal = models.CharField(max_length=15)
    
class VipStatus(models.Model):
    describe = models.CharField(max_length=500)
    requierments = models.CharField(max_length=500)
    price = models.FloatField()
    
    