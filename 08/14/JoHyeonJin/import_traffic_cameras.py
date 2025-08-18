import csv
from django.core.management.base import BaseCommand
from testapp.models import TrafficCamera
from pathlib import Path

class Command(BaseCommand):
    help = 'Import traffic camera data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_path = Path(options['csv_file'])
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR('❌ CSV 파일이 존재하지 않습니다.'))
            return

        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            created_count = 0
            for row in reader:
                TrafficCamera.objects.create(
                    camera_id=row['무인교통단속카메라관리번호'],
                    address=row['소재지지번주소'],
                    latitude=float(row['위도']),
                    longitude=float(row['경도']),
                )
                created_count += 1

            self.stdout.write(self.style.SUCCESS(f'✅ 총 {created_count}개 데이터 삽입 완료'))
