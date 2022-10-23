from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login as login_process
from django.contrib.auth.decorators import login_required
from workOrder import models as woModels
from . import views

@login_required(login_url='/login/')
def home(request):
    emp = woModels.Employee.objects.filter(user__username__exact = request.user.username).first()
    # menuHTML = ""
    # if emp.is_admin or request.user.is_staff:
    #     menuHTML = menuHTML + ' <a aria-current="page" class="d-block text-light p-2" href="/upload/"><i class="icon ion-md-cloud"></i> upload Orders</a> '  
    #     menuHTML = menuHTML + ' <a aria-current="page" class="d-block text-light p-2" href="/upload_payroll/"><i class="icon ion-md-cloud"></i> upload payroll</a> '
    #     menuHTML = menuHTML + '<a aria-current="page" class="d-block text-light p-2" href="/duplicate_order_list/"><i class="icon ion-md-clipboard"></i> Duplicate Orders</a>'
    #     menuHTML = menuHTML + '<a style="color: white;"><hr></a>'
    #     menuHTML = menuHTML + '<a aria-current="page" class="d-block text-light p-2" href="/location_list/"><i class="icon ion-md-business mr-2"></i>  Locations</a>'
    #     menuHTML = menuHTML + '<a aria-current="page" class="d-block text-light p-2" href="/employee_list/"><i class="icon ion-md-people"></i> Employees</a>'
    #     menuHTML = menuHTML + '<a aria-current="page" class="d-block text-light p-2" href="/item_list/"><i class="icon ion-md-business mr-2 lead" lead></i> Items</a>'
    #     menuHTML = menuHTML + '<a style="color: white;"><hr></a>'

    # menuHTML = menuHTML + '<a aria-current="page" class="d-block text-light p-2" href="/order_list/"><i class="icon ion-md-clipboard"></i> Orders</a>'
    # menuHTML = menuHTML + '<a aria-current="page" class="d-block text-light p-2" href="/order_list_sup/' + request.user.username + '"> <i class="icon ion-md-business mr-2 lead" lead></i> WOs by Sup</a>'
        

    return render(
        request,
        'index.html',
        {
        'title':'Home Page',
        'year':datetime.now().year,
        'emp': emp
        }
    )

def login(request):
    state = 0
    message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_process(request, user)
            state = 1
            message = ""
            return redirect('/home/')
        else:
            state = 2
            message = "Username or password is incorrect"
    dic = {'state': state, 'message': message}
    return render(request, 'login.html', dic)