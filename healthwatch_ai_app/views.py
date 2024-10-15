from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.medical_request import MedicalRequest
from .serializers import MedicalRequestSerializer, MedicalCreateRequestSerializer
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class MedicalRequestAPIView(APIView):
    def get(self, request):
      logger.info(f"Received data: {request.data}")
      requests = MedicalRequest.objects.all()
      serializer = MedicalRequestSerializer(requests, many=True)
      return Response(serializer.data)

    def post(self, request):
      serializer = MedicalCreateRequestSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
