from operator import truediv
from pyexpat import model
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Locations(models.Model):
    LocationID = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employeeID = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=100, blank=True, null= True)
    supervisor_name = models.ForeignKey('self', blank=True, null=True,on_delete=models.SET_NULL, db_column='supervisor_name')
    termination_date = models.CharField(max_length=200, blank=True, null= True)
    hire_created =  models.CharField(max_length=200, blank=True, null= True)
    hourly_rate = models.CharField(max_length=200, blank=True, null= True)
    email = models.CharField(max_length=200, blank=True, null= True)
    Location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, db_column='user')
    is_active = models.BooleanField(default=True)
    is_supervisor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ", " + self.last_name

class workOrder(models.Model):
    prismID = models.CharField(max_length=200)
    workOrderId= models.CharField(max_length=200)
    PO = models.CharField(max_length=200)
    POAmount	= models.CharField(max_length=200, blank=True, null=True)
    ConstType	= models.CharField(max_length=200, blank=True, null=True)
    ConstCoordinator= models.CharField(max_length=200, blank=True, null=True)	
    WorkOrderDate= models.CharField(max_length=200, blank=True, null=True)
    EstCompletion= models.CharField(max_length=200, blank=True, null=True)	
    IssuedBy= models.CharField(max_length=200, blank=True, null=True)	
    JobName	= models.CharField(max_length=200, blank=True, null=True)
    JobAddress	= models.CharField(max_length=200, blank=True, null=True)
    SiteContactName	= models.CharField(max_length=200, blank=True, null=True)
    SitePhoneNumber	= models.CharField(max_length=200, blank=True, null=True)
    Comments	= models.CharField(max_length=200, blank=True, null=True)
    Status	= models.CharField(max_length=200, blank=True, null=True)
    CloseDate	= models.CharField(max_length=200, blank=True, null=True)
    WCSup	= models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, db_column='WCSup')
    UploadDate	= models.CharField(max_length=200, blank=True, null=True)
    UserName= models.CharField(max_length=200, blank=True, null=True)
    Location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded = models.BooleanField(default=False)
    linkedOrder = models.CharField(max_length=600, null=True, blank=True)
    

    class Meta:
        unique_together = ('prismID', 'workOrderId','PO')

    def __str__(self):
        return self.prismID + " - " + self.workOrderId + " - " + self.PO

class workOrderDuplicate(models.Model):
    prismID = models.CharField(max_length=200, blank=True, null=True)
    workOrderId= models.CharField(max_length=200, blank=True, null=True)
    PO = models.CharField(max_length=200, blank=True, null=True)
    POAmount	= models.CharField(max_length=200, blank=True, null=True)
    ConstType	= models.CharField(max_length=200, blank=True, null=True)
    ConstCoordinator= models.CharField(max_length=200, blank=True, null=True)	
    WorkOrderDate= models.CharField(max_length=200, blank=True, null=True)
    EstCompletion= models.CharField(max_length=200, blank=True, null=True)	
    IssuedBy= models.CharField(max_length=200, blank=True, null=True)	
    JobName	= models.CharField(max_length=200, blank=True, null=True)
    JobAddress	= models.CharField(max_length=200, blank=True, null=True)
    SiteContactName	= models.CharField(max_length=200, blank=True, null=True)
    SitePhoneNumber	= models.CharField(max_length=200, blank=True, null=True)
    Comments	= models.CharField(max_length=200, blank=True, null=True)
    Status	= models.CharField(max_length=200, blank=True, null=True)
    CloseDate	= models.CharField(max_length=200, blank=True, null=True)
    WCSup	= models.CharField(max_length=200, blank=True, null=True)
    UploadDate	= models.CharField(max_length=200, blank=True, null=True)
    UserName= models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('prismID',
        'workOrderId',
        'PO',
        'POAmount')

    def __str__(self):
        return self.prismID + " - " + self.PO + " - " + self.POAmount
