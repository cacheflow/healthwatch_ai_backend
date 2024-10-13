import os
import random
import pandas as pd
from django.core.management.base import BaseCommand
from healthwatch_ai_app.models.medical_request import MedicalRequest, Duration  # Adjust the import if necessary
from django.conf import settings

class Command(BaseCommand):
    help = 'Load medical requests from a CSV file'

    def handle(self, *args, **kwargs):
        file_paths = ['training_data.csv']
        for path in file_paths:
            df = pd.read_csv(path)
            medical_requests = []
            for index, row in df.iterrows():
                medical_requests.append(MedicalRequest(
                    inmate_id=row['id'],
                    description=row['request_text'],
                    severity=row['severity'],
                    category=row['category'],
                    duration=random.choice(list(Duration)).value
                ))

            MedicalRequest.objects.bulk_create(medical_requests)
            self.stdout.write(self.style.SUCCESS('Successfully loaded medical requests'))

    