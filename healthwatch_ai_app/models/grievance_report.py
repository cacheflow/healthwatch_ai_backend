from django.db import models
from django.core.validators import MinLengthValidator
from enum import Enum
from django.utils import timezone
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import re
import pdb
from datetime import timedelta
from ..ml_models.similar_medical_request_analyzer import SimilarMedicalRequestAnalyzer


class Duration(Enum):
  LESS_THAN_A_DAY = "Less Than A Day"
  ONE_TO_THREE_DAYS = "1 - 3 Days"
  FOUR_TO_SEVEN_DAYS = "4 - 7 Days"
  ONE_TO_FOUR_WEEKS = "1 - 4 Weeks"
  MORE_THAN_A_MONTH = "More than a month"

class MedicalRequestSeverity(Enum):
  HIGH = 'High'
  MEDIUM = 'Medium'
  MODERATE = 'Moderate'
  LOW = 'Low'

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
