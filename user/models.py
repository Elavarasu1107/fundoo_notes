from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    location = models.CharField(max_length=100)
