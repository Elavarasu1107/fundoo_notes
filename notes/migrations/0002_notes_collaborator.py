# Generated by Django 4.1 on 2022-09-10 11:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='collaborator',
            field=models.ManyToManyField(related_name='collaborator', to=settings.AUTH_USER_MODEL),
        ),
    ]
