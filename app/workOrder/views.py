from ast import Try
from contextlib import nullcontext, redirect_stderr
from ctypes.wintypes import WORD
from multiprocessing import context
from os import dup
from telnetlib import WONT
from unittest import TextTestResult
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Employee, workOrder, workOrderDuplicate, Locations
from .resources import workOrderResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import EmployeesForm, LocationsForm, workOrderForm
import logging 


def simple_upload(request):
    countInserted = 0
    countRejected = 0
    duplicateRejected = 0
    if request.method == 'POST':
        #workOrder.objects.all().delete()
        workOrder_resource = workOrderResource()
        dataset = Dataset()
        new_workOrder = request.FILES['myfile']

        if not new_workOrder.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'upload.html', {'countInserted':countInserted, 'countRejected':countRejected})

        imported_data = dataset.load(new_workOrder.read(),format='xlsx')
       
        # return render(request,'upload.html',
        # {'imported_data':imported_data})

        for data in imported_data:  
            rowExist = workOrder.objects.filter(prismID=data[0]).first()
            if rowExist:
                countRejected = countRejected + 1
                try:
                    valueDuplicate = workOrderDuplicate(prismID = data[0],
                        workOrderId = data[1],
                        PO = data[2],
                        POAmount = data[3],
                        ConstType = data[4],
                        ConstCoordinator = data[5],
                        WorkOrderDate = data[6],
                        EstCompletion = data[7],
                        IssuedBy = data[8],
                        JobName = data[9],
                        JobAddress = data[10],
                        SiteContactName = data[11],
                        SitePhoneNumber = data[12],
                        Comments = data[13],
                        Status = data[14],
                        CloseDate = data[15],
                        WCSup = data[16],
                        UploadDate = data[17],
                        UserName = data[18]) 
                    valueDuplicate.save()
                except Exception as e:
                    duplicateRejected = duplicateRejected + 1
            else:
                try:         
                    value = workOrder(
                        prismID = data[0],
                        workOrderId = data[1],
                        PO = data[2],
                        POAmount = data[3],
                        ConstType = data[4],
                        ConstCoordinator = data[5],
                        WorkOrderDate = data[6],
                        EstCompletion = data[7],
                        IssuedBy = data[8],
                        JobName = data[9],
                        JobAddress = data[10],
                        SiteContactName = data[11],
                        SitePhoneNumber = data[12],
                        Comments = data[13],
                        Status = data[14],
                        CloseDate = data[15],
                        WCSup = data[16],
                        UploadDate = data[17],
                        UserName = data[18],
                        uploaded = True
                    )
                    value.save()
                    countInserted = countInserted + 1
                except Exception as e:
                    countRejected = countRejected + 1
                    try:
                        valueDuplicate = workOrderDuplicate(prismID = data[0],
                            workOrderId = data[1],
                            PO = data[2],
                            POAmount = data[3],
                            ConstType = data[4],
                            ConstCoordinator = data[5],
                            WorkOrderDate = data[6],
                            EstCompletion = data[7],
                            IssuedBy = data[8],
                            JobName = data[9],
                            JobAddress = data[10],
                            SiteContactName = data[11],
                            SitePhoneNumber = data[12],
                            Comments = data[13],
                            Status = data[14],
                            CloseDate = data[15],
                            WCSup = data[16],
                            UploadDate = data[17],
                            UserName = data[18]) 
                        valueDuplicate.save()
                    except Exception as e:
                        duplicateRejected = duplicateRejected + 1            
    return render(request,'upload.html', {'countInserted':countInserted, 'countRejected':countRejected,'duplicateRejected':duplicateRejected})

def listOrders(request):

    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    
    if emp:
        if emp.is_admin:
            orders = workOrder.objects.filter()
            return render(request,'order_list.html',
            {'orders': orders})

    if request.user.is_staff:
        orders = workOrder.objects.filter()
        return render(request,'order_list.html',
        {'orders': orders})

    orders = workOrder.objects.filter(Location__isnull=True, WCSup__isnull=True)
    return render(request,'order_list.html',
    {'orders': orders})

   

def order_list_location(request, userID):
    emp = Employee.objects.filter(user__username__exact = userID).first()
    if emp:
        orders = workOrder.objects.filter(Location__LocationID__exact=emp.Location.LocationID, WCSup__isnull=True)
        return render(request,'order_list_location.html',
        {'orders': orders, 'emp': emp })
    else:
        orders = workOrder.objects.filter(Location__LocationID__exact=0, WCSup__isnull=True)
        return render(request,'order_list_location.html',
        {'orders': orders, 'emp': emp })

def order_list_sup(request, userID):  
    emp = Employee.objects.filter(user__username__exact = userID).first()

    if emp:
        orders = workOrder.objects.filter(WCSup__employeeID__exact=emp.employeeID)
        return render(request,'order_list_sup.html',
        {'orders': orders, 'emp': emp })
    else:
        orders = workOrder.objects.filter(WCSup__employeeID__exact=0, Location__isnull=False)
        return render(request,'order_list_sup.html',
        {'orders': orders, 'emp': emp })

def listOrdersFilter(request):
    orders = workOrder.objects.all()
    return render(request,'order_list.html',
    {'orders': orders})

def truncateData(request):
    workOrder.objects.all().delete()
    workOrderDuplicate.objects.all().delete()
    # Locations.objects.all().delete()
    # Employee.objects.all().delete()
    return HttpResponse('<p>Data deleted successfully</p>')

def duplicatelistOrders(request):
    orders = workOrderDuplicate.objects.all()
    return render(request,'duplicate_order_list.html',
    {'orders': orders})

def checkOrder(request, pID):
    orders = workOrder.objects.filter(prismID=pID).first()
    duplicateOrder = workOrderDuplicate.objects.filter(prismID=pID).first()
    return render(request,'checkOrder.html',{'order': orders, 'dupOrder': duplicateOrder})

def order(request, orderID):

    context ={}
    obj = get_object_or_404(workOrder, id = orderID)
 
    form = workOrderForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
  
        context["orders"] = workOrder.objects.filter(Location__isnull=True, WCSup__isnull=True)      
        return render(request, "order_list.html", context)
 
    context["form"] = form
 
    return render(request, "order.html", context)

def updateDupOrder(request,pID, dupID):
    try:
        dupOrder = workOrderDuplicate.objects.filter(id=dupID).first()

        order = workOrder(  id = pID,
                            prismID = dupOrder.prismID,
                            workOrderId = dupOrder.workOrderId,
                            PO = dupOrder.PO,
                            POAmount = dupOrder.POAmount,
                            ConstType = dupOrder.ConstType,
                            ConstCoordinator = dupOrder.ConstCoordinator,
                            WorkOrderDate = dupOrder.WorkOrderDate,
                            EstCompletion = dupOrder.EstCompletion,
                            IssuedBy = dupOrder.IssuedBy,
                            JobName = dupOrder.JobName,
                            JobAddress = dupOrder.JobAddress,
                            SiteContactName = dupOrder.SiteContactName,
                            SitePhoneNumber = dupOrder.SitePhoneNumber,
                            Comments = dupOrder.Comments,
                            Status = dupOrder.Status,
                            CloseDate = dupOrder.CloseDate,
                            WCSup = dupOrder.WCSup,
                            UploadDate = dupOrder.UploadDate,
                            UserName = dupOrder.UserName )
        order.save()
        dupOrder.delete()
        return render(request,'landing.html',{'message':'Order Updated Successfully', 'alertType':'success'})
    except Exception as e:
        return render(request,'landing.html',{'message':'Somenthing went Wrong!', 'alertType':'danger'})

def insertDupOrder(request, dupID):
    try:
        dupOrder = workOrderDuplicate.objects.filter(id=dupID).first()
         
        order = workOrder(  prismID = dupOrder.prismID,
                            workOrderId = dupOrder.workOrderId,
                            PO = dupOrder.PO,
                            POAmount = dupOrder.POAmount,
                            ConstType = dupOrder.ConstType,
                            ConstCoordinator = dupOrder.ConstCoordinator,
                            WorkOrderDate = dupOrder.WorkOrderDate,
                            EstCompletion = dupOrder.EstCompletion,
                            IssuedBy = dupOrder.IssuedBy,
                            JobName = dupOrder.JobName,
                            JobAddress = dupOrder.JobAddress,
                            SiteContactName = dupOrder.SiteContactName,
                            SitePhoneNumber = dupOrder.SitePhoneNumber,
                            Comments = dupOrder.Comments,
                            Status = dupOrder.Status,
                            CloseDate = dupOrder.CloseDate,
                            WCSup = dupOrder.WCSup,
                            UploadDate = dupOrder.UploadDate,
                            UserName = dupOrder.UserName,
                            uploaded = True )
        order.save()
        dupOrder.delete()
        return render(request,'landing.html',{'message':'Order Inserted Successfully', 'alertType':'success'})
    except Exception as e:
        return render(request,'landing.html',{'message':'Somenthing went Wrong!', 'alertType':'danger'})

def deleteDupOrder(request,pID):
    try:
        dupOrder = workOrderDuplicate.objects.filter(id=pID).first()
        dupOrder.delete()
        return render(request,'landing.html',{'message':'Order Discarded Successfully', 'alertType':'success'})
    except Exception as e:
        return render(request,'landing.html',{'message':'Somenthing went Wrong!', 'alertType':'danger'})

def create_order(request):
    context ={}
 
    form = workOrderForm(request.POST or None)
    if form.is_valid():
        form.save()
      
        context["orders"] = workOrder.objects.filter(Location__isnull=True, WCSup__isnull=True)        
        return render(request, "order_list.html", context)
                 
    context['form']= form
    return render(request, "create_order.html", context)

def create_location(request):
    context ={}
 
    form = LocationsForm(request.POST or None)
    if form.is_valid():
        form.save()
        context["dataset"] = Locations.objects.all()         
        return render(request, "location_list.html", context)
         
    context['form']= form
    return render(request, "location.html", context)

def location_list(request):
    context ={}
    context["dataset"] = Locations.objects.all()
         
    return render(request, "location_list.html", context)

def update_location(request, id):

    context ={}
    obj = get_object_or_404(Locations, LocationID = id)
 
    form = LocationsForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        context["dataset"] = Locations.objects.all()         
        return render(request, "location_list.html", context)

    context["form"] = form
 
    return render(request, "update_location.html", context)


def employee_list(request):
    context ={}
 
    context["dataset"] = Employee.objects.all()
         
    return render(request, "employee_list.html", context)
 
def create_employee(request):
    context ={}
 
    form = EmployeesForm(request.POST or None)
    if form.is_valid():
        form.save()
        # Return to Locations List
        context["dataset"] = Employee.objects.all()         
        return render(request, "employee_list.html", context)
         
    context['form']= form
    return render(request, "create_employee.html", context)

def update_employee(request, id):

    context ={}

    obj = get_object_or_404(Employee, employeeID = id)
 
    form = EmployeesForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        context["dataset"] = Employee.objects.all()         
        return render(request, "employee_list.html", context)

    context["form"] = form
 
    return render(request, "update_employee.html", context)

def linkOrderList(request, id):

    context = {}    
    context["order"] = workOrder.objects.filter(id=id).first()
    context["manOrders"] = workOrder.objects.filter(uploaded = False, linkedOrder__isnull = True)

    return render(request, "link_order_list.html", context)


def linkOrder(request, id, manualid):
    context = {}    
    context["order"] = workOrder.objects.filter(id=id).first()
    context["manOrder"] = workOrder.objects.filter(id=manualid).first()
    
    return render(request, "link_order.html", context)


def updateLinkOrder(request, id, manualid):
    try:
        order = workOrder.objects.filter(id=id).first()
        order.linkedOrder = "updated"
        order.save ()

        manOrder = workOrder.objects.filter(id=manualid).first()
        manOrder.linkedOrder = id
        manOrder.save()

        return render(request,'landing.html',{'message':'Order Linked Successfully', 'alertType':'success'})
    except Exception as e:
        return render(request,'landing.html',{'message':'Somenthing went Wrong!', 'alertType':'danger'})