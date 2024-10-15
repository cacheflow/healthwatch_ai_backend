# Generated by Django 5.1.2 on 2024-10-15 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthwatch_ai_app', '0005_medicalrequest_escalated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrequest',
            name='duration_type',
            field=models.TextField(choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], default=('days', 'Days'), max_length=30),
        ),
    ]