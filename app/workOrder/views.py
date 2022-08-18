from ctypes.wintypes import WORD
from telnetlib import WONT
from unittest import TextTestResult
from django.shortcuts import render
from .models import workOrder
from .resources import workOrderResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse

def simple_upload(request):
    if request.method == 'POST':
        workOrder.objects.all().delete()
        workOrder_resource = workOrderResource()
        dataset = Dataset()
        new_workOrder = request.FILES['myfile']

        if not new_workOrder.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'upload.html')

        imported_data = dataset.load(new_workOrder.read(),format='xlsx')
       
        # return render(request,'upload.html',
        # {'imported_data':imported_data})
        contador = 0
        for data in imported_data:
            if contador > 0:
                value = workOrder(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11],
                    data[12],
                    data[13],
                    data[14],
                    data[15],
                    data[16],
                    data[17],
                    data[18]
                )
                value.save()
            contador=contador+1
    return render(request,'upload.html')

def listOrders(request):
    orders = workOrder.objects.all()
    return render(request,'order_list.html',
    {'orders': orders})