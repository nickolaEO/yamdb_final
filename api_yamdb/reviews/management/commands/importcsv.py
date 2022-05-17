import csv
import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, UserProfile

from api_yamdb import settings


class Command(BaseCommand):
    help = (
        'This command helps you to fill CSV data into db. '
        'To perform CSV data migration type the following command: '
        '>>> python manage.py importcsv '
        '--path "filename.csv" '
        '--model_name "model_name" '
        '--app_name "app_name"'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--filename',
            type=str,
            help='file name (with ".csv" extension)'
        )
        parser.add_argument(
            '--model_name',
            type=str,
            help='model name that is used with this ".csv" file'
        )
        parser.add_argument(
            '--app_name',
            ype=str,
            help='django app name'
        )

    def get_csv_file(self, filename):
        file_path = os.path.join(
            settings.BASE_DIR, 'static', 'data', filename
        )
        return file_path

    def handle(self, *args, **options):
        filename = options['filename']
        app_name = options['app_name']
        model_name = options['model_name']
        file_path = self.get_csv_file(filename)
        self.stdout.write(self.style.SUCCESS(f'Reading: {file_path}'))
        _model = apps.get_model(app_name, model_name)
        _model.objects.all().delete()
        line_count = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                header = next(reader)
                for row in reader:
                    if row != '':
                        for i in range(len(row)):
                            if row[i].isdigit():
                                row[i] = int(row[i])
                        _object_dict = {
                            key: value for key, value in zip(header, row)
                        }
                        if 'titles.csv' in filename:
                            category = Category.objects.get(
                                pk=_object_dict['category']
                            )
                            _object_dict['category'] = category
                        if 'review.csv' or 'comments.csv' in filename:
                            author = UserProfile.objects.get(
                                pk=_object_dict['author']
                            )
                            _object_dict['author'] = author
                        print(_object_dict)
                        _model.objects.create(**_object_dict)
                    line_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'{line_count} entries added to {model_name}'
                )
            )
        except FileNotFoundError:
            raise CommandError(f'File {file_path} does not exist')
