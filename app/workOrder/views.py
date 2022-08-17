from ctypes.wintypes import WORD
from django.shortcuts import render
from .models import workOrder
from .resources import workOrderResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse

def simple_upload(request):
    if request.method == 'POST':
        workOrder_resource = workOrderResource()
        dataset = Dataset()
        new_workOrder = request.FILES['myfile']

        if not new_workOrder.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'upload.html')

        imported_data = dataset.load(new_workOrder.read(),format='xlsx')
        for data in imported_data:
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
    return render(request,'upload.html')
