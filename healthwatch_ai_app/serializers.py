from rest_framework import serializers
from .models.medical_request import MedicalRequest, MedicalRequestSeverity

class SeverityMapping: 
  mapping = {
    0: 'Low',
    1: 'Moderate',
    2: 'Medium',
    3: 'High'
  }

  @classmethod 
  def get_label(cls, severity_num):
    return cls.mapping[severity_num].lower()

class MedicalRequestSerializer(serializers.ModelSerializer):
  severity_label = serializers.SerializerMethodField()
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'description', 'category', 'severity_label', 'duration_amount', 'duration_type', 'severity']

  def get_severity_label(self, obj):
    severity = obj.severity
    if isinstance(severity, str):
      return severity
    
    return SeverityMapping.get_label(severity)

class MedicalCreateRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'description', 'category', 'duration_amount', 'duration_type', 'severity']