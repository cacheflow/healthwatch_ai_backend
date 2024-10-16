from rest_framework import serializers
from .models.medical_request import MedicalRequest, MedicalRequestSeverity

class SeverityMapping: 
  mapping = {
    0: 'Low',
    1: 'Moderate',
    2: 'Severe',
    3: 'Very Severe'
  }

  @classmethod 
  def get_label(cls, severity_num):
    return cls.mapping[severity_num].upper()

class MedicalRequestSerializer(serializers.ModelSerializer):
  severity_label = serializers.SerializerMethodField()
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'description', 'category', 'severity_label', 'duration_amount', 'duration_type', 'severity', 'escalating_cost', 'original_cost']

  def get_severity_label(self, obj):
    severity = obj.severity
    if isinstance(severity, str):
      return ' '.join(word.capitalize() for word in severity.split('_'))
    
    return SeverityMapping.get_label(severity)

class MedicalCreateRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'description', 'category', 'duration_amount', 'duration_type', 'severity']