import re
from types import CoroutineType
from django import forms
from .models import Locations, workOrder, workOrderDuplicate, Employee

class LocationsForm(forms.ModelForm):
    LocationID = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'class':'form-control'}))
    city= forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Locations
        fields = [
            "LocationID",
            "name",           
            "description",
             "city",
        ]

class EmployeesForm(forms.ModelForm):   

    supervisor_name = forms.ModelChoiceField(queryset=Employee.objects.filter(is_supervisor=True, is_active=True),required=False)

    class Meta:
        model = Employee
        fields = [
            "employeeID",
            "first_name",           
            "last_name",
             "middle_initial",
             "supervisor_name",
             "termination_date",
             "hire_created",
             "hourly_rate",
             "email",
             "Location",
             "user",
             "is_active",
             "is_supervisor",
             "is_admin"
        ]

class workOrderForm(forms.ModelForm):
    # prismID = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # workOrderId = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'})) 
    # PO = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # POAmount= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # ConstType= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # ConstCoordinator= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # WorkOrderDate= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # EstCompletion= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # IssuedBy= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # JobName= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # JobAddress= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # SiteContactName= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # SitePhoneNumber= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # Comments= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # Status= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # CloseDate= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # UploadDate= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    # UserName= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))

    WCSup = forms.ModelChoiceField(queryset=Employee.objects.filter(is_supervisor=True, is_active=True, user__isnull=False), required=False)

    class Meta:
        model = workOrder
        fields = [
           'id',
            'prismID',
            'workOrderId',
            'PO',
            'POAmount',
            'ConstType',
            'ConstCoordinator',
            'WorkOrderDate',
            'EstCompletion',
            'IssuedBy',
            'JobName',
            'JobAddress',
            'SiteContactName',
            'SitePhoneNumber',
            'Comments',
            'Status',
            'CloseDate',
            'WCSup',
            'UploadDate',
            'UserName',
            "Location",
        ]