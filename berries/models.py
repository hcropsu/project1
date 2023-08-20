from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BerryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    berry_type = models.CharField(max_length=100)
    amount_foraged = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

class Comment(models.Model):
    entry = models.ForeignKey(BerryEntry, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()