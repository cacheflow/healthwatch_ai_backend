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

class MedicalRequest(models.Model):
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now) 
  inmate_id = models.CharField(blank=False, null=False, max_length=16)
  description = models.CharField(max_length=2000)
  category = models.CharField(max_length=30, null=False, blank=False, default='')
  duration_amount = models.FloatField(default=0.5, blank=False)
  duration_type = models.TextField(
    max_length=30,
    default=('days', 'Days'),
    choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')]
  )
  severity = models.CharField(
    default='',
    max_length=30,
    null=False,
    blank=False,
    choices=([(tag.name, tag.value) for tag in MedicalRequestSeverity])
  )
  submission_count = models.IntegerField(default=1) 
  last_submission_at = models.DateTimeField(default=timezone.now)
  escalated = models.BooleanField(default=False)
  
  def find_similar_requests(self, inmate_id, description):
   sanitized_description = re.sub(r'[^A-Za-z0-9\s]', '', description)
   search_query = SearchQuery(sanitized_description)
   two_weeks_ago = timezone.now() - timedelta(weeks=2)
   recent_requests = MedicalRequest.objects.filter(created_at__gte=two_weeks_ago)
   similarity_analyzer = SimilarMedicalRequestAnalyzer
   for request in recent_requests:
    request_description = request.description
    similar = similarity_analyzer.similar(sanitized_description, request_description)
    if similar:
      return request
    return None


  def increment_submission(self):
    self.submission_count += 1
    self.last_submission_at = timezone.now()
    self.save()

  
  def escalate(self):
    if self.submission_count >= 3:
      self.is_escalted = True
      self.save()