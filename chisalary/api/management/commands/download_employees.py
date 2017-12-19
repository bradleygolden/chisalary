from django.core.management.base import BaseCommand
from api.manager import EmployeeManager


class Command(BaseCommand):
    help = 'Downlads employees from the Chicago Data Portal to the database.'

    def handle(self, *args, **options):
        employee_manager = EmployeeManager()
        num_employees = employee_manager.count()
        EmployeeManager().sync_employees(progress_bar=True)
        self.stdout.write(self.style.SUCCESS('Successfully downloaded "{num_employees}" employees.'))
