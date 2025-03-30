# Generated by Django 4.2.20 on 2025-03-29 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_sublinkuser_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(unique=True)),
                ('username', models.CharField(blank=True, max_length=150, null=True)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('language_code', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'telegram_user',
            },
        ),
    ]
