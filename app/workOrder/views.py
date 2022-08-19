from ctypes.wintypes import WORD
from telnetlib import WONT
from unittest import TextTestResult
from django.shortcuts import render
from .models import workOrder, workOrderDuplicate
from .resources import workOrderResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from django.db import IntegrityError

def simple_upload(request):
    countInserted = 0
    countRejected = 0
    duplicateRejected = 0
    if request.method == 'POST':
        # workOrder.objects.all().delete()
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
                    UserName = data[18]
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
    orders = workOrder.objects.all()
    return render(request,'order_list.html',
    {'orders': orders})

def duplicatelistOrders(request):
    orders = workOrderDuplicate.objects.all()
    return render(request,'duplicate_order_list.html',
    {'orders': orders})