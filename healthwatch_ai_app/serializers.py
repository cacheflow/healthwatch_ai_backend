from rest_framework import serializers
from .models.medical_request import MedicalRequest, MedicalRequestSeverity
from .models.user import User

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

class InmateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'role', 'id')

class MedicalRequestSerializer(serializers.ModelSerializer):
  severity_label = serializers.SerializerMethodField()
  created_at_label = serializers.SerializerMethodField()
  inmate = InmateSerializer()

  class Meta:
    model = MedicalRequest
    fields = ['inmate_description', 'category', 'created_at_label',
              'severity_label', 'duration_amount', 'duration_type', 'id', 'provider_summary',
              'severity', 'escalating_cost', 'original_cost', 'inmate', 'issue'
              ]

  def get_severity_label(self, obj):
    severity = obj.severity
    if isinstance(severity, str):
      return ' '.join(word.capitalize() for word in severity.split('_'))
    
    return SeverityMapping.get_label(severity)

  def get_created_at_label(self, obj):
    created_at = obj.created_at
    return created_at.strftime('%B %d, %Y at %I:%M %p')

class MedicalCreateRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'inmate_description', 'category', 'duration_amount', 'duration_type', 'severity', 'issue']