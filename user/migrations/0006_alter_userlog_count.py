# Generated by Django 4.1 on 2022-09-06 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_userlog_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]