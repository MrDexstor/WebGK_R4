# Generated by Django 5.1.5 on 2025-01-27 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TelegramBot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestDataMatrixLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(max_length=20)),
                ('in_value', models.CharField(max_length=100)),
                ('request_status', models.CharField(max_length=50)),
                ('datamatrix_count', models.IntegerField()),
                ('request_reason', models.CharField(max_length=1000)),
                ('requets_is_processed', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TelegramBot.tguser')),
            ],
        ),
    ]
