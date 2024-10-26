from django.contrib import admin
from timesheet.models import *


# Register your models here.

class TimesheetAdmin(admin.ModelAdmin):
        list_display = ('date', 'EmployeeID', 'Status')
        search_fields = ['date', 'Status',]


admin.site.register(Timesheet, TimesheetAdmin)