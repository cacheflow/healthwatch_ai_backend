from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.medical_request import MedicalRequest
from .serializers import MedicalRequestSerializer, MedicalCreateRequestSerializer
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .ml_models import MedicalRequestClassifier
from .ml_models import SimilarMedicalRequestAnalyzer
from django.db.models import Q
import random

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class MedicalRequestAPIView(APIView):
    def get(self, request):
      logger.info(f"Received data: {request.data}")
      requests = MedicalRequest.objects.order_by('-created_at')[:30]
      serializer = MedicalRequestSerializer(requests, many=True)
      return Response(serializer.data)

    
    def post(self, request):
      inmate_id = request.data["inmate_id"]
      description = request.data['description']
      similar_request = MedicalRequest().find_similar_requests(inmate_id, description)
      serializer = MedicalCreateRequestSerializer(data=request.data)
      if serializer.is_valid():
        medical_request = serializer.save()
        validated_data = serializer.validated_data
        data = serializer.validated_data.pop('description')
        prediction_data = MedicalRequestClassifier.predict(data)
        prediction = ''
        for curr in prediction_data:
          if 'label' in curr:
            prediction = curr['label']
        labels = {
          'LABEL_3': 'very_severe',
          'LABEL_2': 'severe',
          'LABEL_1': 'moderate',
          'LABEL_0': 'mild',
        }
        medical_request.severity=labels[prediction] or labels['LABEL_1']
        original_cost = random.randrange(200, 600)
        medical_request.escalating_cost=original_cost * 2
        medical_request.original_cost=original_cost
        medical_request.save()
        medical_request_serializer = MedicalRequestSerializer(medical_request)
        json_data = JSONRenderer().render(serializer.data)
        
        return Response(medical_request_serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
