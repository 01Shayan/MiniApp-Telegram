# Generated by Django 4.2.20 on 2025-03-29 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_telegramuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
