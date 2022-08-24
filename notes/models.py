from django.db import models
from user.models import User


class Notes(models.Model):
    title = models.TextField()
    description = models.TextField()
    color = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
