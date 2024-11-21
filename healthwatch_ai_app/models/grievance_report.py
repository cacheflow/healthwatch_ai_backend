from django.db import models
from django.core.validators import MinLengthValidator
from enum import Enum
from django.utils import timezone
from django.db.models import Q


class GrievanceReport(models.Model):
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now) 
  category = models.CharField(max_length=100, blank=False, null=False, default='')
  
  description = models.CharField(max_length=2000)
  due_date = models.DateTimeField(default=timezone.now) 
  inmate = models.ForeignKey('healthwatch_ai_app.User', on_delete=models.CASCADE, null=True, default=True)
  status = models.CharField(
    default='pending',
    max_length=30,
    choices=[('pending', 'Pending'), 
             ('in_progress', 'In Progress'), ('resolved', 'Resolved'), 
             ]
  )
  
  submission_count = models.IntegerField(default=1) 
  last_submission_at = models.DateTimeField(default=timezone.now)
  escalated = models.BooleanField(default=False)
