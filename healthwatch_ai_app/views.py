from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.medical_request import MedicalRequest
from .serializers import MedicalRequestSerializer, MedicalCreateRequestSerializer

class MedicalRequestAPIView(APIView):
    def get(self, request):
      requests = MedicalRequest.objects.all()
      serializer = MedicalRequestSerializer(requests, many=True)
      return Response(serializer.data)

    def post(self, request):
      serializer = MedicalCreateRequestSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
