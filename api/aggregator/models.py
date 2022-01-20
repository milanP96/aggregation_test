from django.db import models

# Create your models here.


class Event(models.Model):
    timestamp = models.DateTimeField()
    domain = models.CharField(max_length=64)
    requests_number = models.IntegerField()
