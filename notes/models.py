from django.db import models
from user.models import User


class Labels(models.Model):
    title = models.TextField()
    color = models.TextField()
    font = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Notes(models.Model):
    title = models.TextField()
    description = models.TextField()
    color = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField(Labels, related_name='label')
