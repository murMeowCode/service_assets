from django.db import models

class FAQItem(models.Model):
    question = models.CharField(max_length=150)
    answer = models.CharField(max_length=500)
