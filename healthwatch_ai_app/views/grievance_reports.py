from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
import pdb
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from healthwatch_ai_app.models import GrievanceReport, User

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class GrievanceReportsAPIView(APIView):
    def post(self, request, *args, **kwargs):
      try: 
        
        inmate_id = request.data["inmate_id"]
        description = request.data['description']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        unit_number = request.data['unit_number']
        assignment = request.data['assignment']
        requested_outcome = request.data['requested_outcome']
        category = request.data['category']
        inmate = User.objects.filter(inmate_id=inmate_id, identifier=inmate_id).first()
        if inmate is None and inmate_id is not None: 
           inmate = User.objects.create(inmate_id=inmate_id, identifier=inmate_id, first_name=first_name, last_name=last_name)
           
        grievance_report = GrievanceReport.objects.create(
        description=description, 
        first_name=first_name, last_name=last_name, 
        unit_number=unit_number, assignment=assignment, 
        inmate=inmate,
        requested_outcome=requested_outcome, category=category)

        json_data = JSONRenderer().render({
           'description': grievance_report.description,
           'first_name': grievance_report.first_name,
           'last_name': grievance_report.last_name,
           'unit_number': grievance_report.unit_number,
           'requested_outcome': grievance_report.requested_outcome
        })
          
        return Response(json_data, status=status.HTTP_201_CREATED)
      except Exception as e:
         pdb.set_trace()
         return Response({'error': 'An error occurred'}, status=500)
      