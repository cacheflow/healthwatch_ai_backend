from django.db import models
from django.core.validators import MinLengthValidator
from enum import Enum
# Create your models here.

class Duration(Enum):
  LESS_THAN_A_DAY = "Less Than A Day"
  ONE_TO_THREE_DAYS = "1 - 3 Days"
  FOUR_TO_SEVEN_DAYS = "4 - 7 Days"
  ONE_TO_FOUR_WEEKS = "1 - 4 Weeks"
  MORE_THAN_A_MONTH = "More than a month"

class MedicalRequestSeverity(Enum):
  HIGH = 'High'
  MEDIUM = 'Medium'
  LOW = 'Low'

class MedicalRequest(models.Model):
  inmate_id = models.CharField(blank=False, null=False, max_length=16)
  description = models.CharField(max_length=2000)
  category = models.CharField(max_length=30, null=False, blank=False, default='')
  duration_amount = models.FloatField(default=0.5, blank=False)
  duration_type = models.CharField(
    max_length=10,
    default=('days', 'Days'),
    choices=[('days', 'Days'), ('months', 'Months'), ('years', 'Years')]
  )
  severity = models.CharField(
    default='',
    max_length=30,
    null=False,
    blank=False,
    choices=([(tag.name, tag.value) for tag in MedicalRequestSeverity])
  )