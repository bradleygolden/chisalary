from django.core.management.base import BaseCommand
from api.manager import EmployeesManager


class Command(BaseCommand):
    help = 'Downlads employees from the Chicago Data Portal to the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Max number of employees to download',
        )

    def handle(self, *args, **options):
        employees_manager = EmployeesManager()
        limit = options.get('limit')

        if not limit:
            limit = employees_manager.count()
        self.stdout.write(self.style.SUCCESS(f'Downloading "{limit}" employees.'))
        employees_manager.sync_employees(limit=limit, progress_bar=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully downloaded "{limit}" employees.'))
