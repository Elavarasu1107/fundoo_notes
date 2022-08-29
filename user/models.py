from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import JWT


class User(AbstractUser):
    phone = models.BigIntegerField()
    location = models.CharField(max_length=100)
    is_verified = models.IntegerField(default=0)

    @property
    def token(self):
        return JWT.encode({"user_id": self.id, "username": self.username})
