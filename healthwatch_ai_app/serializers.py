from rest_framework import serializers
from .models.medical_request import MedicalRequest

class MedicalRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'description', 'category', 'duration_amount', 'duration_type', 'severity']

class MedicalCreateRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'description', 'category', 'duration_amount', 'duration_type', 'severity']
