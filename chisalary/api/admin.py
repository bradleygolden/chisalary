from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    list_filter = ('full_or_part_time', 'salary_or_hourly')


admin.site.register(Employee, EmployeeAdmin)
