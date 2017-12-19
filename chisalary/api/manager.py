from nameparser import HumanName
from .models import Employee
from django.conf import settings
import requests
import logging
from .exceptions import ChicagoDataPortalError
import click

logger = logging.getLogger(__name__)


class EmployeeManager:

    def __init__(self):
        pass

    def query(self, *args, **kwargs):
        headers = kwargs.get('headers', {})
        headers['X-App-Token'] = settings.APP_TOKEN

        r = requests.get(settings.EMPLOYEE_URL, headers=headers, **kwargs)

        if not r.status_code == 200:
            raise ChicagoDataPortalError

        return r

    def count(self, *args, **kwargs):
        _count = settings.LIMIT
        if not settings.LIMIT:
            _count = self.query(params={'$select': 'count(name)'}, **kwargs).json()[0].get('count_name')

        if not _count:
            raise ChicagoDataPortalError('Unable to get count employee count')

        return _count

    def employees(self):
        count = self.count()
        logger.info(f'Total employees found: {count}')

        r = self.query(params={'$limit': self.count()})

        if not r.status_code == 200:
            raise ChicagoDataPortalError('Unable to get employees from portal.')

        employees = r.json()

        logger.info(f'Retreived {len(employees)} employees from {settings.EMPLOYEE_URL}')

        return [self.clean(employee) for employee in employees]

    def clean(self, employee):
        name = HumanName(employee.get('name'))
        employee['last_name'] = name.last
        employee['first_name'] = name.first
        employee['middle_name'] = name.middle
        employee.pop('name')
        return employee

    def sync_employee(self, employee):

            try:
                existing_employee = Employee.objects.filter(first_name__exact=employee.get('first_name')) \
                    .filter(middle_name__exact=employee.get('middle_name')) \
                    .filter(last_name__exact=employee.get('last_name')) \
                    .get()

                existing_employee.job_titles = employee.get('job_titles')
                existing_employee.department = employee.get('department')
                existing_employee.full_or_part_time = employee.get('full_or_part_time')
                existing_employee.salary_or_hourly = employee.get('salary_or_hourly')
                existing_employee.typical_hours = employee.get('typical_hours')
                existing_employee.annual_salary = employee.get('annual_salary')
                existing_employee.hourly_rate = employee.get('hourly_rate')

                existing_employee.save()

                logger.debug(f'Updating employee {existing_employee.__dict__}')

            except Employee.DoesNotExist as ex:
                new_employee = Employee(**employee)
                new_employee.save()

    def sync_employees(self, employees=None, progress_bar=False):
        if not employees:
            employees = self.employees()

        if progress_bar:
            with click.progressbar(employees, length=len(employees)) as bar:
                for employee in bar:
                    self.sync_employee(employee)
        else:
            self.sync_employee(employee)
