# Generated by Django 5.1.2 on 2024-10-15 03:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthwatch_ai_app', '0007_alter_medicalrequest_duration_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalrequest',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 15, 3, 19, 36, 88097, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='medicalrequest',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 15, 3, 19, 36, 91122, tzinfo=datetime.timezone.utc)),
        ),
    ]