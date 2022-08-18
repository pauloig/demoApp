from operator import truediv
from pyexpat import model
from django.db import models
# Create your models here.



class workOrder(models.Model):
    prismID = models.CharField(max_length=200)
    workOrderId= models.CharField(max_length=200, blank=True, null=True)
    PO = models.CharField(max_length=200)
    POAmount	= models.CharField(max_length=200)
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
        unique_together = ('prismID', 'PO','POAmount')



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