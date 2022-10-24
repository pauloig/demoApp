from ast import Try, parse
from contextlib import nullcontext, redirect_stderr
from ctypes.wintypes import WORD
from datetime import datetime
from multiprocessing import context
from os import WIFCONTINUED, dup
import re
from telnetlib import WONT
from unittest import TextTestResult
from urllib import response
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Employee, payrollDetail, workOrder, workOrderDuplicate, Locations, item, itemPrice, payroll, internalPO
from .resources import workOrderResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse, FileResponse
from django.db import IntegrityError
from .forms import EmployeesForm, InternalPOForm, ItemForm, ItemPriceForm, LocationsForm, workOrderForm
from sequences import get_next_value, Sequence
from datetime import date
from django.utils.dateparse import parse_date
import datetime
import logging 
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.template.loader import get_template
from xhtml2pdf import pisa
from .classes import itemPriceList
from decimal import Decimal
from django.db.models import Max




def simple_upload(request):

    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

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
                        Status = '1',
                        CloseDate = data[15],
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
    return render(request,'upload.html', {'countInserted':countInserted, 'countRejected':countRejected,'duplicateRejected':duplicateRejected, 'emp': emp})


def upload_payroll(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    countInserted = 0
    countRejected = 0
    countUpdated = 0
    if request.method == 'POST':
        dataset = Dataset()
        new_payroll = request.FILES['myfile']

        if not new_payroll.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'upload_payroll.html', {'countInserted':countInserted, 'countRejected':countRejected, 'countUpdated' : countUpdated  })

        imported_data = dataset.load(new_payroll.read(),format='xlsx')
      

        for data in imported_data:             
            try:         
                value = payroll(
                    location = data[0],
                    employee = data[3],
                    date =  data[2],
                    prismID = data[18],
                    workOrderId= data[19],
                    PO = data[20],
                    RT = data[5],
                    OT = data[6],
                    DT = data[7],
                    IT = data[8],
                    RTPrice = data[9],
                    OTPrice = data[10],
                    bonus = data[11],
                    production = data[12],
                    ownVehicle = data[13],
                    onCall = data[14],
                    payroll = data[15],
                    supervisor = data[16],
                    address = data[21],
                    itemTotal = data[46],
                    invoice = data[47],
                    pdfDaily = data[48]
                )
                value.save()

                if (data[23] != 0 and data[23] != " " and data[23] is not None):
                    value2 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[22],
                        quantity = data[23],
                        )
                    value2.save()

                if (data[25] != 0 and data[25] != " " and data[25] is not None):
                    value3 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[24],
                        quantity = data[25],
                        )
                    value3.save()

                if (data[27] != 0 and data[27] != " " and data[27] is not None):
                    value4 = payrollDetail(
                       location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[26],
                        quantity = data[27],
                        )
                    value4.save()

                if (data[29] != 0 and data[29] != " " and data[29] is not None):
                    value5 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[28],
                        quantity = data[29],
                        )
                    value5.save()

                if (data[31] != 0 and data[31] != " " and data[31] is not None):
                    value6 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[30],
                        quantity = data[31],
                        )
                    value6.save()
                
                if (data[33] != 0 and data[33] != " " and data[33] is not None):
                    value7 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[32],
                        quantity = data[33],
                        )
                    value7.save()
                
                if (data[35] != 0 and data[35] != " " and data[35] is not None):
                    value8 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[34],
                        quantity = data[35],
                        )
                    value8.save()

                if (data[37] != 0 and data[37] != " " and data[37] is not None):
                    value9 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[36],
                        quantity = data[37],
                        )
                    value9.save()

                if (data[39] != 0 and data[39] != " " and data[39] is not None):
                    value10 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[38],
                        quantity = data[39],
                        )
                    value10.save()
                
                if (data[41] != 0 and data[41] != " " and data[41] is not None):
                    value11 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[40],
                        quantity = data[41],
                        )
                    value11.save()

                if (data[43] != 0 and data[43] != " " and data[43] is not None):
                    value12 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[42],
                        quantity = data[43],
                        )
                    value12.save()

                if (data[45] != 0 and data[45] != " " and data[45] is not None):
                    value13 = payrollDetail(
                        location = data[0],
                        employee = data[3],
                        date =  data[2],
                        prismID = data[18],
                        workOrderId= data[19],
                        PO = data[20],
                        item = data[44],
                        quantity = data[45],
                        )
                    value13.save()

                # get de WO to update Location and Supervisor
                try:
                    wo = workOrder.objects.filter(prismID = data[18], workOrderId = data[19], PO = data[20]).first()
                    loc = Locations.objects.filter(LocationID = data[0]).first()
                    emp = Employee.objects.filter(employeeID = data[16] ).first()
                    if (wo and loc and emp):
                        wo.Location = loc
                        wo.WCSup = emp
                        wo.Status = '2'
                        wo.save()

                        # update WorkOrderId on Payroll
                        value.woId = wo
                        value.save()

                        countUpdated =  countUpdated + 1
                except Exception as e:
                    countUpdatedR =  countUpdatedR + 1

                countInserted = countInserted + 1
            except Exception as e:
                countRejected = countRejected + 1                
                       
    return render(request,'upload_payroll.html', {'countInserted':countInserted, 'countRejected':countRejected, 'countUpdated' : countUpdated, 'emp':emp })



def listOrders(request):
    locationList = Locations.objects.all()
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    estatus = "0"
    loc = "0"
    

    if request.method == "POST":
        estatus = request.POST.get('status')
        loc = request.POST.get('location') 
        locationObject = Locations.objects.filter(LocationID=loc).first()
    
    if emp:
        if emp.is_admin:     
            if estatus == "0" and loc == "0":   
                orders = workOrder.objects.exclude(linkedOrder__isnull = False, uploaded = False )        
            else:
                if estatus != "0" and loc != "0":
                    orders = workOrder.objects.filter(Status = estatus, Location = locationObject).exclude(linkedOrder__isnull = False, uploaded = False )     
                else:
                    if estatus != "0":
                        orders = workOrder.objects.filter(Status = estatus).exclude(linkedOrder__isnull = False, uploaded = False ) 
                    else:
                        orders = workOrder.objects.filter(Location = locationObject).exclude(linkedOrder__isnull = False, uploaded = False ) 
            return render(request,'order_list.html',{'orders': orders, 'emp':emp, 'location': locationList})

    if request.user.is_staff:
        if estatus == "0" and loc == "0":    
            orders = workOrder.objects.exclude(linkedOrder__isnull = False, uploaded = False )  
        else:
            if estatus != "0" and loc != "0":
                orders = workOrder.objects.filter(Status = estatus, Location = locationObject).exclude(linkedOrder__isnull = False, uploaded = False )  
            else:
                if estatus != "0":
                    orders = workOrder.objects.filter(Status = estatus).exclude(linkedOrder__isnull = False, uploaded = False )  
                else:
                    orders = workOrder.objects.filter(Location = locationObject).exclude(linkedOrder__isnull = False, uploaded = False )  

        return render(request,'order_list.html',{'orders': orders, 'emp':emp, 'location': locationList})


    # orders = workOrder.objects.filter(Location__isnull=True, WCSup__isnull=True)
    if estatus == "0" and loc == "0":   
        orders = workOrder.objects.filter(WCSup__isnull=True).exclude(linkedOrder__isnull = False, uploaded = False )
    else:
        if estatus != "0" and loc != "0":
            orders = workOrder.objects.filter(WCSup__isnull=True, Location = locationObject, Status = estatus).exclude(linkedOrder__isnull = False, uploaded = False )
        else:
            if estatus != "0":
                orders = workOrder.objects.filter(WCSup__isnull=True, Status = estatus).exclude(linkedOrder__isnull = False, uploaded = False )
            else:
                orders = workOrder.objects.filter(WCSup__isnull=True, Location = locationObject).exclude(linkedOrder__isnull = False, uploaded = False )

    return render(request,'order_list.html',{'orders': orders, 'emp':emp, 'location': locationList})

   

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
    # emp = Employee.objects.filter(user__username__exact = userID).first()
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    if emp:
        orders = workOrder.objects.filter(WCSup__employeeID__exact=emp.employeeID).exclude(linkedOrder__isnull = False, uploaded = False )
        return render(request,'order_list_sup.html',
        {'orders': orders, 'emp': emp })
    else:
        orders = workOrder.objects.filter(WCSup__employeeID__exact=0, Location__isnull=False).exclude(linkedOrder__isnull = False, uploaded = False )
        return render(request,'order_list_sup.html',
        {'orders': orders, 'emp': emp })

def listOrdersFilter(request):
    orders = workOrder.objects.all()
    return render(request,'order_list.html',
    {'orders': orders})

def truncateData(request):
    workOrder.objects.all().delete()
    workOrderDuplicate.objects.all().delete()
    payroll.objects.all().delete()
    payrollDetail.objects.all().delete()
    # Locations.objects.all().delete()
    # Employee.objects.all().delete()
    return HttpResponse('<p>Data deleted successfully</p>')

def duplicatelistOrders(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    orders = workOrderDuplicate.objects.all()
    return render(request,'duplicate_order_list.html',{'orders': orders, 'emp':emp})

def checkOrder(request, pID):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    orders = workOrder.objects.filter(prismID=pID).first()
    duplicateOrder = workOrderDuplicate.objects.filter(prismID=pID).first()
    return render(request,'checkOrder.html',{'order': orders, 'dupOrder': duplicateOrder, 'emp':emp})

def order(request, orderID):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
    obj = get_object_or_404(workOrder, id = orderID)
 
    form = workOrderForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/order_list/')
 
    context["form"] = form
    context["emp"] = emp
    return render(request, "order.html", context)

def updateDupOrder(request,pID, dupID):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

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
                            Status = '1',
                            CloseDate = dupOrder.CloseDate,
                            UploadDate = datetime.datetime.now(),
                            UserName = dupOrder.UserName,
                            uploaded = True )
        order.save()
        dupOrder.delete()
        return render(request,'landing.html',{'message':'Order Updated Successfully', 'alertType':'success', 'emp':emp})
    except Exception as e:
        return render(request,'landing.html',{'message':'Somenthing went Wrong!', 'alertType':'danger', 'emp':emp})

def insertDupOrder(request, dupID):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

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
                            Status = '1',
                            CloseDate = dupOrder.CloseDate,
                            UploadDate = dupOrder.UploadDate,
                            UserName = dupOrder.UserName,
                            uploaded = True )
        order.save()
        dupOrder.delete()
        return render(request,'landing.html',{'message':'Order Inserted Successfully', 'alertType':'success','emp':emp})
    except Exception as e:
        print(e)
        return render(request,'landing.html',{'message':'Somenthing went Wrong! ' + str(e), 'alertType':'danger','emp':emp})

def deleteDupOrder(request,pID):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    try:
        dupOrder = workOrderDuplicate.objects.filter(id=pID).first()
        dupOrder.delete()
        return render(request,'landing.html',{'message':'Order Discarded Successfully', 'alertType':'success', 'emp':emp})
    except Exception as e:
        return render(request,'landing.html',{'message':'Somenthing went Wrong!', 'alertType':'danger','emp':emp})

def create_order(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
    woID = 'E-'
    form = workOrderForm(request.POST or None, initial={'prismID': woID,'workOrderId': woID, 'PO': woID})
    if form.is_valid():
        woNumber = Sequence("wo") 
        woID = str(woNumber.get_next_value())
        woID = 'E-' + woID 
        form.instance.prismID = woID
        form.instance.workOrderId = woID
        form.instance.PO = woID
        form.instance.Status = '1'
        form.instance.UploadDate = datetime.datetime.now()
        form.save()
        return HttpResponseRedirect('/order_list/')
         
    context['form']= form
    context['emp'] = emp
    return render(request, "create_order.html", context)

def create_location(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
 
    form = LocationsForm(request.POST or None)
    if form.is_valid():
        form.save()
        context["dataset"] = Locations.objects.all()   
        context["emp"]=emp      
        return render(request, "location_list.html", context)
         
    context['form']= form
    context["emp"]=emp
    return render(request, "location.html", context)

def location_list(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
    context["dataset"] = Locations.objects.all()
    context["emp"] = emp
         
    return render(request, "location_list.html", context)

def update_location(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
    obj = get_object_or_404(Locations, LocationID = id)
 
    form = LocationsForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        context["dataset"] = Locations.objects.all() 
        context["emp"] = emp       
        return render(request, "location_list.html", context)

    context["form"] = form
    context["emp"] = emp
    return render(request, "update_location.html", context)


def employee_list(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
 
    context["dataset"] = Employee.objects.all()
    context["emp"]= emp
    return render(request, "employee_list.html", context)
 
def create_employee(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    context ={}

    form = EmployeesForm(request.POST or None)

    if form.is_valid():
        empSeq = Sequence("emp", initial_value=1500) 
        empID = str(empSeq.get_next_value())       
        form.instance.employeeID = empID
        form.save()
        # Return to Locations List
        return HttpResponseRedirect('/employee_list/')
        # context["dataset"] = Employee.objects.all()     
        # context["emp"] = emp    
        # return render(request, "employee_list.html", context)
         
    context['form']= form
    context["emp"] = emp
    return render(request, "create_employee.html", context)

def update_employee(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(Employee, employeeID = id)
 
    form = EmployeesForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        context["dataset"] = Employee.objects.all()  
        context["emp"] = emp       
        return render(request, "employee_list.html", context)

    context["form"] = form
    context["emp"] = emp
    return render(request, "update_employee.html", context)

def linkOrderList(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context = {}    
    context["order"] = workOrder.objects.filter(id=id).first()
    context["manOrders"] = workOrder.objects.filter(uploaded = False, linkedOrder__isnull = True)
    context["emp"] = emp
    return render(request, "link_order_list.html", context)


def linkOrder(request, id, manualid):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context = {}    
    context["order"] = workOrder.objects.filter(id=id).first()
    context["manOrder"] = workOrder.objects.filter(id=manualid).first()
    context["emp"] = emp
    return render(request, "link_order.html", context)


def updateLinkOrder(request, id, manualid):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    try:
        order = workOrder.objects.filter(id=id).first()
        order.linkedOrder = "updated"
        order.save ()

        manOrder = workOrder.objects.filter(id=manualid).first()
        manOrder.linkedOrder = id
        manOrder.save()

        return render(request,'landing.html',{'message':'Order Linked Successfully', 'alertType':'success','emp':emp})
    except Exception as e:
        return render(request,'landing.html',{'message':'Somenthing went Wrong!', 'alertType':'danger','emp':emp})


def item_list(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context = {}    
    context["items"] = item.objects.all()
    context["emp"] = emp
    
    return render(request, "item_list.html", context)


def create_item(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
 
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.datetime.now()
        form.save()               
        return HttpResponseRedirect("/item_list/")
         
    context['form']= form
    context["emp"]=emp
    return render(request, "create_item.html", context)

def update_item(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(item, itemID = id)
 
    form = ItemForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/item_list/")

    context["form"] = form
    context["emp"] = emp
    return render(request, "update_item.html", context)


def item_price(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context = {}    
    context["item"] = item.objects.filter(itemID = id).first()

    context["item_location"] = itemPrice.objects.filter(item = id)
    context["emp"] = emp

    return render(request, "item_price.html", context)

def create_item_price(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
 
    form = ItemPriceForm(request.POST or None)
    if form.is_valid():
        # form.instance.createdBy = request.user.username
        # form.instance.created_date = datetime.datetime.now()
        form.save()               
        return HttpResponseRedirect("/item_list/")
         
    context['form']= form
    context["emp"] = emp
    return render(request, "create_item_price.html", context)


def update_item_price(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(itemPrice, id = id )
 
    form = ItemPriceForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/item_list/")
        # it = itemPrice.objects.filter(id = id).first()
        # return HttpResponseRedirect("/item_list/" + it.item__itemID)
        # return item_price(request,it.item__itemID)

    context["form"] = form
    context["emp"] = emp
    return render(request, "update_item_price.html", context)

def po_list(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context = {}    
    wo = workOrder.objects.filter(id=id).first()
    context["order"] = wo
    context["po"] = internalPO.objects.filter(woID = wo)
    context["emp"] = emp
    return render(request, "po_order_list.html", context)


def update_po(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(internalPO, id = id )
 
    form = InternalPOForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/order_list/")

    context["form"] = form
    context["emp"] = emp
    return render(request, "update_po.html", context)

def create_po(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}
    wo = workOrder.objects.filter(id=id).first()
    form = InternalPOForm(request.POST or None, initial={'woID': wo})
    if form.is_valid():
        # form.instance.createdBy = request.user.username
        # form.instance.created_date = datetime.datetime.now()
        form.save()               
        return HttpResponseRedirect("/order_list/")
         
    context['form']= form
    context["emp"] = emp
    return render(request, "create_po.html", context)

def report_pdf(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textObj = c.beginText()
    textObj.setTextOrigin(inch,inch)
    textObj.setFont("Helvetica",14)

    lines = [
        "Wiring Connection, Inc.",
        "1718 W. 139th Street",
        "Gardena, CA 90249",
        "",
        "",
        "Bill To",
        "Charter Communications"
        "8120 Camino Arroyo"
        "Gilroy, CA 95020"
        ""
        "",
        "PO#          PO Amount   Comp. Date     Coordinator     Work Order     Const. Type      PID#",
        "4501026881   27668.50                  Tony Aguilar      1544467       Hospitality    3333478",
        "Item                    Description                           Qty        Rate             Amount",
        "US06            Place Each Fiber Cable in Occupied Duct       1,606      1.30             2,087.80",
        "US28            Proof and Place, per conduit foot               962      0.50               481.00",
        "NS005           Materials and Fees Pass-through               2,080      1.10             2,288.00",
    ]
    
    for line in lines:
        textObj.textLine(line)

    c.drawText(textObj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='report.pdf')



def estimate(request, id):
    context = {}    
    wo = workOrder.objects.filter(id=id).first()

    context["payroll"] = payroll.objects.filter(woId = wo, itemTotal__gte = 1 ).first()

    payItems = payrollDetail.objects.filter(prismID =wo.prismID , workOrderId = wo.workOrderId , PO = wo.PO)
    context["items"] = payItems

    context["estimate"] = True

    itemHtml = ''
    total = 0 
    linea = 0
    try:
        for data in payItems:
            linea = linea + 1
            amount = 0
            itemO = item.objects.filter(itemID = data.item).first()
            loc = Locations.objects.filter(LocationID = data.location).first()
            if itemO:
                priceO = itemPrice.objects.filter(item = itemO, location = loc).first()

                if priceO:
                    amount = Decimal(str(data.quantity)) * Decimal(str(priceO.price))
                    total = total + amount
                    itemHtml = itemHtml + " <tr>"
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="20%" align="center"> ' + itemO.itemID + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px; padding-left: 2px;" width="43%" align="left">    ' + itemO.name + '</td> '
                    itemHtml = itemHtml +  ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="13%" align="center">' + priceO.price + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + str(amount) + '</td> '
                    itemHtml = itemHtml + ' </tr> '
                else:
                    itemHtml = itemHtml + ' <tr> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="20%" align="center">' + data.item + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="43%" align="left">' + data.item + '</td> '
                    itemHtml = itemHtml +  ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="13%" align="center">' + 0  + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center"> 0 </td> '
                    itemHtml = itemHtml + ' </tr> '
                    
            else:
                itemHtml = itemHtml + ' <tr> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="20%" align="center">' + data.item + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="43%" align="left">' + data.item + '</td> '
                itemHtml = itemHtml +  ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="13%" align="center">' + 0 + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center"> 0 </td> '
                itemHtml = itemHtml + ' </tr> '
    except Exception as e:
        print(e)

    # obtengo las internal PO
    internal = internalPO.objects.filter(woID = wo)

    for data in internal:
        linea = linea + 1
        amount = Decimal(str(data.total)) 
        total = total + amount
        itemHtml = itemHtml + ' <tr> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="20%" align="center"> N/A </td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + data.product + '</td> '
        itemHtml = itemHtml +  ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="13%" align="center"> N/A </td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">'  + data.total + '</td>'
        itemHtml = itemHtml + ' </tr> '

    for i in range(21-linea):
        itemHtml = itemHtml + '<tr>'
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="20%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="43%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="12%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="13%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="12%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '</tr> '
        
    context["itemPrice"] = itemHtml
    context["total"] = total


    template_path = 'invoice_template.html'

    template= get_template(template_path)

    if (wo.pre_invoice != 0 and wo.pre_invoice != " " and wo.pre_invoice is None):         
        pre = Sequence("preinvoice")
        wo.pre_invoice = str(pre.get_next_value())
        wo.Status=4
        wo.save()
    
   

    wo2 = workOrder.objects.filter(id=id).first()
    fileName = "estimate-" + wo2.pre_invoice + ".pdf"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + fileName

    context["order"] = wo2

    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)


    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response     

def invoice(request, id):
    context = {}    
    wo = workOrder.objects.filter(id=id).first()

    context["payroll"] = payroll.objects.filter(woId = wo, itemTotal__gte = 1 ).first()

    context["items"] = payrollDetail.objects.filter(prismID =wo.prismID , workOrderId = wo.workOrderId , PO = wo.PO)

    payItems = payrollDetail.objects.filter(prismID =wo.prismID , workOrderId = wo.workOrderId , PO = wo.PO)
    context["items"] = payItems

    context["estimate"] = False

    itemHtml = ''
    total = 0 
    linea = 0
    try:
        for data in payItems:
            linea = linea + 1
            amount = 0
            itemO = item.objects.filter(itemID = data.item).first()
            loc = Locations.objects.filter(LocationID = data.location).first()
            if itemO:
                priceO = itemPrice.objects.filter(item = itemO, location = loc).first()

                if priceO:
                    amount = Decimal(str(data.quantity)) * Decimal(str(priceO.price))
                    total = total + amount
                    itemHtml = itemHtml + " <tr>"
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="20%" align="center"> ' + itemO.itemID + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px; padding-left: 2px;" width="43%" align="left">   ' + itemO.name + '</td> '
                    itemHtml = itemHtml +  ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="13%" align="center">' + priceO.price + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + str(amount) + '</td> '
                    itemHtml = itemHtml + ' </tr> '
                else:
                    itemHtml = itemHtml + ' <tr> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="20%" align="center">' + data.item + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="43%" align="left">' + data.item + '</td> '
                    itemHtml = itemHtml +  ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="13%" align="center">' + 0  + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center"> 0 </td> '
                    itemHtml = itemHtml + ' </tr> '
                    
            else:
                itemHtml = itemHtml + ' <tr> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="20%" align="center">' + data.item + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="43%" align="left">' + data.item + '</td> '
                itemHtml = itemHtml +  ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="13%" align="center">' + 0 + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center"> 0 </td> '
                itemHtml = itemHtml + ' </tr> '
    except Exception as e:
        print(e)

    # obtengo las internal PO
    internal = internalPO.objects.filter(woID = wo)

    for data in internal:
        linea = linea + 1
        amount = Decimal(str(data.total)) 
        total = total + amount
        itemHtml = itemHtml + ' <tr> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="20%" align="center"> N/A </td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + data.product + '</td> '
        itemHtml = itemHtml +  ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="13%" align="center"> N/A </td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #444; border-right:1px solid #444; padding-top: 3px;" width="12%" align="center">'  + data.total + '</td>'
        itemHtml = itemHtml + ' </tr> '


    for i in range(20-linea):
        itemHtml = itemHtml + '<tr>'
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="20%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="43%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="12%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="13%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '<td style="border-left:1px solid #444; border-right:1px solid #444;" width="12%" align="center">&nbsp;</td> '
        itemHtml = itemHtml + '</tr> '
        
    context["itemPrice"] = itemHtml
    context["total"] = total

    template_path = 'invoice_template.html'

    template= get_template(template_path)

    if (wo.invoice != 0 and wo.invoice != " " and wo.invoice is None):         
        pre = Sequence("invoice")
        wo.invoice = str(pre.get_next_value())
        wo.Status=5
        wo.save()

    wo2 = workOrder.objects.filter(id=id).first()

    fileName = "invoice-" + wo2.invoice + ".pdf"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + fileName

    context["order"] = wo2

    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)


    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response   


def estimate_preview(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context = {}    
    wo = workOrder.objects.filter(id=id).first()

    context["order"] = wo
    context["emp"] = emp

    context["payroll"] = payroll.objects.filter(woId = wo, itemTotal__gte = 1 ).first()

    payItems = payrollDetail.objects.filter(prismID =wo.prismID , workOrderId = wo.workOrderId , PO = wo.PO)
    context["items"] = payItems

    context["estimate"] = True

    itemHtml = ''
    total = 0 
    linea = 0
    try:
        for data in payItems:
            linea = linea + 1
            amount = 0
            itemO = item.objects.filter(itemID = data.item).first()
            loc = Locations.objects.filter(LocationID = data.location).first()
            if itemO:
                priceO = itemPrice.objects.filter(item = itemO, location = loc).first()

                if priceO:
                    amount = Decimal(str(data.quantity)) * Decimal(str(priceO.price))
                    total = total + amount
                    itemHtml = itemHtml + ' <tr> '                  
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="20%" align="center">' + itemO.itemID + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + itemO.name + '</td> '
                    itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="13%" align="center">' + priceO.price + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">'  + str(amount) + '</td>'
                    itemHtml = itemHtml + ' </tr> '
                else:
                    itemHtml = itemHtml + ' <tr> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px;" width="20%" align="center">'  + data.item + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + data.item + '</td> '
                    itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px;" width="13%" align="center">' + 0 + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px;" width="12%" align="center">'  + 0 + '</td>'
                    itemHtml = itemHtml + ' </tr> '
                    
            else:
                itemHtml = itemHtml + ' <tr> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="20%" align="center">'  + data.item + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #44e9e9e94; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + data.item + '</td> '
                itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="13%" align="center">' + 0 + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">'  + 0 + '</td>'
                itemHtml = itemHtml + ' </tr> '
    except Exception as e:
        print(e)

    # obtengo las internal PO
    internal = internalPO.objects.filter(woID = wo)

    for data in internal:
        linea = linea + 1
        amount = Decimal(str(data.total)) 
        total = total + amount
        itemHtml = itemHtml + ' <tr> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="20%" align="center">'  + 'N/A'+ '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + data.product + '</td> '
        itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="13%" align="center">' +'N/A' + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">'  + data.total + '</td>'
        itemHtml = itemHtml + ' </tr> '

   
    for i in range(21-linea):
        itemHtml = itemHtml + ' <tr> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="20%" align="center">'  + '&nbsp;'+ '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + '&nbsp;' + '</td> '
        itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">' + '&nbsp;' + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="13%" align="center">' +'&nbsp;' + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">'  + '&nbsp;' + '</td>'
        itemHtml = itemHtml + ' </tr> '
        
    context["itemPrice"] = itemHtml
    context["total"] = total

    return render(request, "pre_invoice.html", context)

def invoice_preview(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context = {}    
    wo = workOrder.objects.filter(id=id).first()

    context["order"] = wo
    context["emp"] = emp
    context["payroll"] = payroll.objects.filter(woId = wo, itemTotal__gte = 1 ).first()

    payItems = payrollDetail.objects.filter(prismID =wo.prismID , workOrderId = wo.workOrderId , PO = wo.PO)
    context["items"] = payItems

    context["estimate"] = False

    itemHtml = ''
    total = 0 
    linea = 0
    
    try:
        for data in payItems:
            linea = linea + 1
            amount = 0
            itemO = item.objects.filter(itemID = data.item).first()
            loc = Locations.objects.filter(LocationID = data.location).first()
            if itemO:
                priceO = itemPrice.objects.filter(item = itemO, location = loc).first()

                if priceO:
                    amount = Decimal(str(data.quantity)) * Decimal(str(priceO.price))
                    total = total + amount
                    itemHtml = itemHtml + ' <tr> '                  
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="20%" align="center">' + itemO.itemID + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + itemO.name + '</td> '
                    itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="13%" align="center">' + priceO.price + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">'  + str(amount) + '</td>'
                    itemHtml = itemHtml + ' </tr> '
                else:
                    itemHtml = itemHtml + ' <tr> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px;" width="20%" align="center">'  + data.item + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + data.item + '</td> '
                    itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px;" width="13%" align="center">' + 0 + '</td> '
                    itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9;; padding-top: 3px;" width="12%" align="center">'  + 0 + '</td>'
                    itemHtml = itemHtml + ' </tr> '
                    
            else:
                itemHtml = itemHtml + ' <tr> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="20%" align="center">'  + data.item + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #44e9e9e94; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + data.item + '</td> '
                itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="13%" align="center">' + 0 + '</td> '
                itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">'  + 0 + '</td>'
                itemHtml = itemHtml + ' </tr> '
    except Exception as e:
        print(e)

    # obtengo las internal PO
    internal = internalPO.objects.filter(woID = wo)

    for data in internal:
        linea = linea + 1
        amount = Decimal(str(data.total)) 
        total = total + amount
        itemHtml = itemHtml + ' <tr> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="20%" align="center">'  + 'N/A'+ '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + data.product + '</td> '
        itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">' + data.quantity + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="13%" align="center">' +'N/A' + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">'  + data.total + '</td>'
        itemHtml = itemHtml + ' </tr> '

   
    for i in range(21-linea):
        itemHtml = itemHtml + ' <tr> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="20%" align="center">'  + '&nbsp;'+ '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px; padding-left: 2px;" width="43%" align="left">' + '&nbsp;' + '</td> '
        itemHtml = itemHtml +  ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">' + '&nbsp;' + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="13%" align="center">' +'&nbsp;' + '</td> '
        itemHtml = itemHtml + ' <td style="border-left:1px solid #e9e9e9; border-right:1px solid #e9e9e9; padding-top: 3px;" width="12%" align="center">'  + '&nbsp;' + '</td>'
        itemHtml = itemHtml + ' </tr> '
        
    context["itemPrice"] = itemHtml
    context["total"] = total

    return render(request, "pre_invoice.html", context)


def pre_invoice2(request, id):

    context = {}    
    wo = workOrder.objects.filter(id=id).first()
    context["order"] = wo

    return render(request, "pre_invoice2.html", context)




def upload_item(request):
    countInserted = 0
    countRejected = 0
    countUpdated = 0
    if request.method == 'POST':
        dataset = Dataset()
        new_item = request.FILES['myfile']

        if not new_item.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'upload_item.html', {'countInserted':countInserted, 'countRejected':countRejected  })

        imported_data = dataset.load(new_item.read(),format='xlsx')
      

        for data in imported_data:             
            try:         
                value = item(
                    itemID = data[0],
                    name = data[1],
                    description =  data[2],
                    is_active = True ,
                    created_date = datetime.datetime.now()                   
                )
                value.save()

                countInserted = countInserted + 1
            except Exception as e:
                countRejected = countRejected + 1                
                       
    return render(request,'upload_item.html', {'countInserted':countInserted, 'countRejected':countRejected })


def upload_item_price(request):
    countInserted = 0
    countRejected = 0
    countUpdated = 0
    if request.method == 'POST':
        dataset = Dataset()
        new_item = request.FILES['myfile']

        if not new_item.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'upload_itemDetail.html', {'countInserted':countInserted, 'countRejected':countRejected  })

        imported_data = dataset.load(new_item.read(),format='xlsx')
      

        for data in imported_data:             
            try:         
                itemp = item.objects.filter(itemID = data[0]).first()
                loca = Locations.objects.filter(LocationID = data[1]).first()

                if itemp and loca:
                    value = itemPrice(
                        item = itemp,
                        location = loca,
                        pay_perc =  data[2],
                        price = data[3],
                        emp_payout = data[4],
                        rate  = data[5]                
                    )
                    value.save()

                    countInserted = countInserted + 1
            except Exception as e:
                print(e)
                countRejected = countRejected + 1                
                       
    return render(request,'upload_itemDetail.html', {'countInserted':countInserted, 'countRejected':countRejected })


def upload_employee(request):
    countInserted = 0
    countRejected = 0
    countUpdated = 0
    if request.method == 'POST':
        dataset = Dataset()
        new_item = request.FILES['myfile']

        if not new_item.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'upload_employee.html', {'countInserted':countInserted, 'countRejected':countRejected  })

        imported_data = dataset.load(new_item.read(),format='xlsx')
      

        for data in imported_data:             
            try:         
                value = Employee(
                    employeeID = data[0],
                    first_name = data[1],
                    last_name = data[2],
                    hourly_rate = data[3],
                    email = data[4],
                    is_active = True
                )
                value.save()

                countInserted = countInserted + 1
            except Exception as e:
                countRejected = countRejected + 1                
                       
    return render(request,'upload_employee.html', {'countInserted':countInserted, 'countRejected':countRejected })