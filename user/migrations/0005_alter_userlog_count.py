# Generated by Django 4.1 on 2022-09-06 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userlog_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
