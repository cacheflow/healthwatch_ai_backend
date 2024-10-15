import os
import random
import pandas as pd
from django.core.management.base import BaseCommand
from healthwatch_ai_app.models.medical_request import MedicalRequest, Duration  # Adjust the import if necessary
from django.conf import settings

class Command(BaseCommand):
    help = 'Load medical requests from a CSV file'

    def handle(self, *args, **kwargs):
        file_paths = ['/Users/lex/Documents/healthwatch-ai-client/sample_inmate_medical_requests_16.csv']
        duration_amount = random.randrange(1, 31)
        duration_type = random.choice([('days', 'Days'), ('months', 'Months'), ('years', 'Years')])
        for path in file_paths:
            df = pd.read_csv(path)
            medical_requests = []
            for index, row in df.iterrows():

                medical_requests.append(MedicalRequest(
                    inmate_id=row['id'],
                    description=row['request_text'],
                    severity=row['severity'],
                    category=row['category'],
                    duration_type=duration_type,
                    duration_amount=duration_amount
                ))

            MedicalRequest.objects.bulk_create(medical_requests)
            self.stdout.write(self.style.SUCCESS('Successfully loaded medical requests'))

    