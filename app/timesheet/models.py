from contextlib import nullcontext
from operator import truediv
from pyexpat import model
from random import choices
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from workOrder import models as catalogModel

prodStatus_choice = (
    (1, 'Draft'),
    (2, 'Sent'),
    (3, 'Pending'),
    (4, 'Approved'),
    (5, 'Rejected')
)

class Timesheet(models.Model):
    EmployeeID = models.ForeignKey(catalogModel.Employee, on_delete=models.CASCADE, db_column ='EmployeeID', null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    start_time = models.IntegerField(null=True, blank=True)
    start_lunch_time = models.IntegerField(null=True, blank=True)
    end_lunch_time = models.IntegerField(null=True, blank=True)
    end_time = models.IntegerField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)
    regular_hours = models.FloatField(null=True, blank=True)
    ot_hour = models.FloatField(null=True, blank=True)
    double_time = models.FloatField(null=True, blank=True)
    start_mileage = models.IntegerField(null=True, blank=True)
    end_mileage = models.IntegerField(null=True, blank=True)
    total_mileage = models.IntegerField(null=True, blank=True)
    Status = models.IntegerField(default=1, choices = prodStatus_choice)   
    Location = models.ForeignKey(catalogModel.Locations, on_delete=models.CASCADE, db_column ='Location', null=False, blank=False)  
    comments = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)
    Period = models.ForeignKey(catalogModel.period, on_delete=models.CASCADE, db_column ='Period', null=True, blank=True)
    crew = models.ForeignKey(catalogModel.Daily, on_delete=models.CASCADE, db_column ='crew', null=True, blank=True)
    #crew = models.IntegerField(null=True, blank=True)
    transferred_date = models.DateTimeField(null=True, blank=True)
    tranferredBy = models.CharField(max_length=60, blank=True, null=True)
    

    def __str__(self):
        return  str(self.date)
    
    class Meta:
        unique_together = ('EmployeeID','date')
    #COnsultar cuantas veces puede enviar el empleado información al dia
