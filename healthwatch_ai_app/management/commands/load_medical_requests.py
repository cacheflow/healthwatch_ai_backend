import os
import random
import pandas as pd
from django.utils import timezone
from django.core.management.base import BaseCommand
from healthwatch_ai_app.models.user import User
from healthwatch_ai_app.models.medical_request import MedicalRequest, Duration 
from django.conf import settings

class Command(BaseCommand):
    help = 'Load medical requests from a CSV file'

    def handle(self, *args, **kwargs):
        user_data = [
            {
                'username': 'inmate1',
                'first_name': 'Michael',
                'last_name': 'Brown',
                'role': 'inmate',
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            },
            {
                'username': 'inmate2',
                'first_name': 'Chris',
                'last_name': 'Jackson',
                'role': 'inmate',
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            },
            {
                'username': 'medstaff1',
                'first_name': 'Jack',
                'last_name': 'Johnson',
                'role': 'medical_staff',
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            },
            {
                'username': 'medstaff2',
                'first_name': 'Betty',
                'last_name': 'Boo',
                'role': 'medical_staff',
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            }
        ]

        for user in user_data: 
            created_user = User.objects.create(
                username=user['username'], 
                first_name=user['first_name'], 
                last_name=user['last_name'], 
                role=user['role'], 
            )
            created_user.set_password('password')
            created_user.save()
        file_paths = ['/Users/lex/Documents/healthwatch_ai_backend/dummy_medical_requests.csv']
        MedicalRequest.objects.filter().delete()
        duration_amount = random.randrange(1, 31)
        duration_type = random.choice([('days', 'Days'), ('months', 'Months'), ('years', 'Years')])
        inmate_ids = User.objects.filter(role='inmate').values('id')
        for path in file_paths:
            df = pd.read_csv(path)
            medical_requests = []
            for index, row in df.iterrows():

                medical_requests.append(MedicalRequest(
                    inmate_id=random.choice(inmate_ids)['id'],
                    description=row['description'],
                    severity=row['severity'],
                    category=row['category'],
                    original_cost=row['original_cost'],
                    escalating_cost=row['escalating_cost'],
                    duration_type=duration_type,
                    duration_amount=duration_amount
                ))
            
            MedicalRequest.objects.bulk_create(medical_requests)
            self.stdout.write(self.style.SUCCESS('Successfully loaded medical requests'))

    