from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.medical_request import MedicalRequest
from .serializers import MedicalRequestSerializer, MedicalCreateRequestSerializer
from .ml_models import MedicalRequestClassifier
from .ml_models import SimilarMedicalRequestAnalyzer
from django.db.models import Q

class MedicalRequestAPIView(APIView):
    def get(self, request):
      requests = MedicalRequest.objects.all()
      serializer = MedicalRequestSerializer(requests, many=True)
      return Response(serializer.data)

    
    def post(self, request):
      inmate_id = request.data["inmate_id"]
      description = request.data['description']
      similar_request = MedicalRequest().find_similar_requests(inmate_id, description)
      if similar_request:
        similar_request.increment_submission()
        medical_request_serializer = MedicalRequestSerializer(medical_request)
        return Response(medical_request_serializer.data, status=status.HTTP_201_CREATED)
      
      serializer = MedicalCreateRequestSerializer(data=request.data)
      if serializer.is_valid():
        medical_request = serializer.save()
        validated_data = serializer.validated_data
        data = serializer.validated_data.pop('description')
        prediction = MedicalRequestClassifier.predict(data)
        medical_request.severity=prediction
        medical_request.save()
        medical_request_serializer = MedicalRequestSerializer(medical_request)
        json_data = JSONRenderer().render(serializer.data)
        
        return Response(medical_request_serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
