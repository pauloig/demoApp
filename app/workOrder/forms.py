import re
from types import CoroutineType
from django import forms
from .models import Locations, item, workOrder, workOrderDuplicate, Employee, itemPrice, internalPO, period, DailyEmployee, DailyItem, Daily, vendor, subcontractor

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
    employeeID = forms.CharField(required=False)

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
             "is_admin",
             "is_superAdmin"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employeeID'].disabled = True

class workOrderForm(forms.ModelForm):
    prismID = forms.CharField(label="Prism ID", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    workOrderId = forms.CharField(label="Work Order ID", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'})) 
    PO = forms.CharField(label="Purchase Order", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    POAmount= forms.CharField(label="Purchase Order Amount",max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    ConstType= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    ConstCoordinator= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'size':60}), required=False)
    WorkOrderDate= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    EstCompletion= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    IssuedBy= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    JobName= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    JobAddress= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    SiteContactName= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    SitePhoneNumber= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    Comments= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    #Status= forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}))
    CloseDate= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    UploadDate= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    UserName= forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

    WCSup = forms.ModelChoiceField(label="Supervisor",queryset=Employee.objects.filter(is_supervisor=True, is_active=True, user__isnull=False), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    createdBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    created_date = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

    class Meta:
        model = workOrder
        fields = [
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
            "created_date",
            "createdBy"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prismID'].disabled = True
        self.fields['workOrderId'].disabled = True
        self.fields['PO'].disabled = True       
        self.fields['created_date'].disabled = True
        self.fields['createdBy'].disabled = True 



class ItemForm(forms.ModelForm):
    itemID = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'class':'form-control'}))
    is_active= forms.BooleanField(required=False)
    createdBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    created_date = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    class Meta:
        model = item
        fields = [
            "itemID",
            "name",           
            "description",
            "is_active",
            "createdBy",
            "created_date"
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['createdBy'].disabled = True
        self.fields['created_date'].disabled = True
       

class ItemPriceForm(forms.ModelForm):
    
    class Meta:
        model = itemPrice
        fields = [
           'item',
            'location',
            'pay_perc',
            'price',
            'emp_payout',
            'rate',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].disabled = True

class InternalPOForm(forms.ModelForm):    

    supervisor = forms.ModelChoiceField(queryset=Employee.objects.filter(is_active=True, is_supervisor = True), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    pickupEmployee = forms.ModelChoiceField(queryset=Employee.objects.filter(is_active=True), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    product = forms.CharField(label="Product",max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    quantity = forms.CharField(label="Quantity",max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    total = forms.CharField(label="Total",max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    

    class Meta:
        model = internalPO
        fields = [
            'woID',
            'supervisor',
            'pickupEmployee',
            'product',
            'quantity',
            'total',
            'subcontractor',            
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['woID'].disabled = True

class periodForm(forms.ModelForm):

    class Meta:
        model = period
        fields = [
            'periodID',
            'periodYear',
            'fromDate',
            'toDate',
            'payDate',
            'weekRange',
            'status'
        ]


class dailydForm(forms.ModelForm):   

    class Meta:
        model = Daily
        fields = [
            'crew',
            'Period',
            'Location',
            'day',
            'pdfDaily'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['crew'].disabled = True

class dailySupForm(forms.ModelForm):   

    class Meta:
        model = Daily
        fields = [
            'woID',
            'supervisor',
            'Location',
            'day',
            'pdfDaily'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['woID'].disabled = True        


class DailyEmpForm(forms.ModelForm):

    class Meta:
        model = DailyEmployee
        fields = [
            'DailyID',
            'EmployeeID',
            'per_to_pay',
            'on_call',
            'bonus',
            'start_time',
            'start_lunch_time',
            'end_lunch_time',
            'end_time',
            'total_hours'
        ]

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs')
        super().__init__(*args, **kwargs)
        self.fields['DailyID'].disabled = True
        self.fields['EmployeeID'].queryset = qs

class DailyItemForm(forms.ModelForm):
    """ itemID = forms.ModelChoiceField(queryset=itemPrice.objects.filter(location__LocationID = ),required=False)"""

    class Meta:
        model = DailyItem
        fields = [
            'DailyID',
            'itemID',
            'quantity',            
        ]

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs')
        super().__init__(*args, **kwargs)
        self.fields['DailyID'].disabled = True
        self.fields['itemID'].queryset = qs

class venforForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class':'form-control'}))
    contact = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'form-control'}))
    contactPosition = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'form-control'}))
    contactPhone = forms.CharField(max_length=50, widget=forms.Textarea(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class':'form-control'}))
    is_active = forms.BooleanField(required=False)
    created_date = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class':'form-control'}))
    createdBy = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class':'form-control'}))


    class Meta:
        model = vendor
        fields = [
            'name',
            'address',
            'contact', 
            'contactPosition',
            'contactPhone',
            'description',
            'is_active',
            'created_date',
            'createdBy'        
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_date'].disabled = True
        self.fields['createdBy'].disabled = True
      
