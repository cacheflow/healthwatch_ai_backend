# Generated by Django 5.1.2 on 2024-10-14 23:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthwatch_ai_app', '0004_remove_medicalrequest_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalrequest',
            name='escalated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicalrequest',
            name='last_submission_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='medicalrequest',
            name='submission_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='medicalrequest',
            name='duration_type',
            field=models.CharField(choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], default=('days', 'Days'), max_length=30),
        ),
        migrations.AlterField(
            model_name='medicalrequest',
            name='severity',
            field=models.CharField(choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('MODERATE', 'Moderate'), ('LOW', 'Low')], default='', max_length=30),
        ),
    ]