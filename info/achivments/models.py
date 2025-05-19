from django.db import models

class Achivments(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)

class AchivmentsUser(models.Model):
    user_id = models.IntegerField()
    achivments_id = models.ForeignKey(Achivments, on_delete=models.DO_NOTHING)