from nameparser import HumanName
from .models import Employee
from django.conf import settings
import requests
import logging
from .exceptions import ChicagoDataPortalError
import click

logger = logging.getLogger(__name__)


class EmployeeManager:

    def __init__(self, employee):
        self.employee = employee

    def clean_name(self):
        name = HumanName(self.employee.get('name'))
        self.employee['last_name'] = name.last
        self.employee['first_name'] = name.first
        self.employee['middle_name'] = name.middle
        self.employee.pop('name')
        return self

    def clean_annual_salary(self):
        if 'annual_salary' in self.employee and self.employee['annual_salary']:
            self.employee['annual_salary'] = self.employee['annual_salary']
        return self

    def clean_hourly_rate(self):
        if 'hourly_rate' in self.employee and self.employee['hourly_rate']:
            self.employee['hourly_rate'] = self.employee['hourly_rate']
        return self

    def clean(self):
        return self.clean_name().clean_hourly_rate().clean_annual_salary()


class EmployeesManager:

    def __init__(self):
        pass

    def query(self, *args, **kwargs):
        headers = kwargs.get('headers', {})
        if settings.APP_TOKEN:
            headers['X-App-Token'] = settings.APP_TOKEN

        r = requests.get(settings.EMPLOYEE_URL, headers=headers, **kwargs)

        if not r.status_code == 200:
            logger.critical('Data portal error: %s', r.content)
            raise ChicagoDataPortalError

        return r

    def count(self, *args, **kwargs):
        _count = self.query(params={'$select': 'count(name)'}, **kwargs).json()[0].get('count_name')

        if not _count:
            raise ChicagoDataPortalError('Unable to get count employee count')

        return _count

    def employees(self, limit=None):
        if limit is None:
            limit = self.count()
        logger.info('Total employees found: %d', limit)

        r = self.query(params={'$limit': limit})

        if not r.status_code == 200:
            logger.critical('Data portal error: %s', r.content)
            raise ChicagoDataPortalError('Unable to get employees from portal.')

        _employees = [EmployeeManager(employee).clean().employee for employee in r.json()]

        logger.info('Retreived %d employees from %s', len(_employees), settings.EMPLOYEE_URL)

        return _employees

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

                logger.debug('Updating employee %s', existing_employee.__dict__)

            except Employee.DoesNotExist as ex:
                new_employee = Employee(**employee)
                new_employee.save()

    def sync_employees(self, employees=None, progress_bar=False, limit=None):
        if not employees:
            employees = self.employees(limit=limit)

        if progress_bar:
            with click.progressbar(employees, length=len(employees)) as bar:
                for employee in bar:
                    self.sync_employee(employee)
        else:
            for employee in employees:
                self.sync_employee(employee)
