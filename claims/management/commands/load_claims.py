from typing import Any
from django.core.management.base import BaseCommand
from claims.models import Claim, ClaimDetail
from decimal import Decimal
from datetime import datetime
import csv
class Command(BaseCommand):
    help = 'Load claims data from CSV files into the database'

    def add_arguments(self, parser):
        parser.add_argument('claims_csv', type=str, help='Path to the claims CSV file')
        parser.add_argument('details_csv', type=str, help='Path to the claim details CSV file')
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL('Deleting existing Claim Data'))
        Claim.objects.all().delete()
        claim_file_path=options['claims_csv']
        self.stdout.write(self.style.MIGRATE_LABEL(f"Loading data from {claim_file_path}"))
        with open(claim_file_path,mode='r',encoding='utf-8') as file:
            reader=csv.DictReader(file,delimiter="|")
            for row in reader:
                Claim.objects.create(
                    id=row['id'],
                    patient_name=row['patient_name'],
                    billed_amount=Decimal(row['billed_amount']),
                    paid_amount=Decimal(row['paid_amount']),
                    status=row['status'],
                    insurer_name=row['insurer_name'],
                    discharge_date=datetime.strptime(row['discharge_date'], '%Y-%m-%d').date(),
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded claims.'))
        self.stdout.write(self.style.MIGRATE_LABEL('Deleting existing Detail Data'))
        ClaimDetail.objects.all().delete()
        detail_file_path=options['details_csv']
        self.stdout.write(self.style.MIGRATE_LABEL(f"Loading data from {detail_file_path}"))
        with open(detail_file_path,mode='r',encoding='utf-8') as file:
            reader=csv.DictReader(file,delimiter="|")
            for row in reader:
                try:
                    fk_claim=Claim.objects.get(pk=row['claim_id'])
                    ClaimDetail.objects.create(
                        id=row['id'],
                        claim=fk_claim,
                        cpt_codes=row['cpt_codes'],
                        denial_reason=row['denial_reason'] or None
                    )
                except Claim.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Skipping detail record {row['id']}: Couldn't find the corresponding claim"))
        self.stdout.write(self.style.SUCCESS('Successfully loaded and linked all claim details.'))