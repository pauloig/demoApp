from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login as login_process
from django.contrib.auth.decorators import login_required
from workOrder import models as woModels
from . import views


def calculate_payroll(locID):
    per = woModels.period.objects.filter(status=1).first()    

    if locID > 0:
        loca = woModels.Locations.objects.filter(LocationID = locID)
    else:
        loca = woModels.Locations.objects.all()
    
    TotPayroll = 0
    TotInvoice = 0
    Totperc = 0
    for locItem in loca:
        daily = woModels.Daily.objects.filter(Location = locItem, Period = per)     
        regular_time = 0
        over_time = 0
        double_time = 0
        total_time = 0
        rt = 0
        ot = 0
        dt = 0
        bonus = 0
        on_call = 0
        prod = 0
        gran_total = 0
        payroll = 0
        ownvehicle = 0
        invoice = 0
        payroll2= 0
        perc = 0
        for dailyItem in daily:            
            production = woModels.DailyItem.objects.filter(DailyID=dailyItem).count()

            dailyemp = woModels.DailyEmployee.objects.filter(DailyID=dailyItem)

            for i in dailyemp:
                if production <= 0:
                    regular_time += i.regular_hours
                    over_time += i.ot_hour
                    double_time += i.double_time
                    total_time += i.total_hours
                    if i.EmployeeID.hourly_rate != None:
                        rt += (i.regular_hours * float(i.EmployeeID.hourly_rate))
                        ot += ((i.ot_hour * (float(i.EmployeeID.hourly_rate)*1.5)))
                        dt += ((i.double_time * (float(i.EmployeeID.hourly_rate)*2)))

                if i.bonus != None:
                    bonus += i.bonus
                    
                if i.on_call != None:
                    on_call += i.on_call

                if i.payout != None:
                    payroll += i.payout

            
            dailyprod =  woModels.DailyItem.objects.filter(DailyID=dailyItem)
            total = 0
            
            ov = 0
            for j in dailyprod:                
                total += j.total
                if j.itemID.price != None:
                    invoice += (j.quantity * float(j.itemID.price))
                else:
                    invoice += (j.quantity * 0)
                
                if j.itemID.emp_payout != None:
                    payroll2 += (j.quantity * float(j.itemID.emp_payout))
                else:
                    payroll2 += (j.quantity * 0)

            if dailyItem.own_vehicle != None:
                ov = ((total * dailyItem.own_vehicle) / 100)
                ownvehicle += ov
            prod += (total)

        if invoice > 0:                    
            perc = (payroll * 100) / invoice
        
        TotPayroll += payroll
        TotInvoice += invoice
        if TotInvoice > 0:
            Totperc = (TotPayroll*100) / TotInvoice

    return round(float(TotPayroll),2), TotInvoice, Totperc


def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
       return 0


@login_required(login_url='/login/')
def home(request):
    context = {}    
    emp = woModels.Employee.objects.filter(user__username__exact = request.user.username).first()
    per = woModels.period.objects.filter(status=1).first()
    totPayroll=0 
    totInvoice=0 
    totPerc= 0
    OrderStatus = []
    OrderStatusValues = []
    status = []
    #Get total Orders by Rol
    if emp.is_admin  or request.user.is_staff:
        totalOrders = woModels.workOrder.objects.all().count()
        totPayroll, totInvoice, totPerc = calculate_payroll(0)
        s1 = woModels.workOrder.objects.filter(Status=1).count()
        if s1 > 0:
            OrderStatus.append('Not Started')
            OrderStatusValues.append(s1)
            status.append({'status':'Not Started', 'total': s1})
        s2 = woModels.workOrder.objects.filter(Status=2).count()
        if s2 > 0:
            OrderStatus.append('Work in Progress')
            OrderStatusValues.append(s2)
            status.append({'status':'Work in Progress', 'total': s2})
        s3 = woModels.workOrder.objects.filter(Status=3).count()
        if s3 > 0:
            OrderStatus.append('Pending Docs')
            OrderStatusValues.append(s3)
            status.append({'status':'Pending Docs', 'total': s3})
        s4 = woModels.workOrder.objects.filter(Status=4).count()
        if s4 > 0:
            OrderStatus.append('Pending Revised WO')
            OrderStatusValues.append(s4)
            status.append({'status':'Pending Revised WO', 'total': s4})        
        s5 = woModels.workOrder.objects.filter(Status=5).count()
        if s5 > 0:
            OrderStatus.append('Invoiced')
            OrderStatusValues.append(s5)
            status.append({'status':'Invoiced', 'total': s5})
    else:
        totalOrders = woModels.workOrder.objects.filter(Location = emp.Location).count()
        totPayroll, totInvoice, totPerc = calculate_payroll(emp.Location.LocationID)
        s1 = woModels.workOrder.objects.filter(Status=1, Location = emp.Location).count()
        if s1 > 0:
            OrderStatus.append('Not Started')
            OrderStatusValues.append(s1)
            status.append({'status':'Not Started', 'total': s1})
        s2 = woModels.workOrder.objects.filter(Status=2, Location = emp.Location).count()
        if s2 > 0:
            OrderStatus.append('Work in Progress')
            OrderStatusValues.append(s2)
            status.append({'status':'Work in Progress', 'total': s2})
        s3 = woModels.workOrder.objects.filter(Status=3, Location = emp.Location).count()
        if s3 > 0:
            OrderStatus.append('Pending Docs')
            OrderStatusValues.append(s3)
            status.append({'status':'Pending Docs', 'total': s3})
        s4 = woModels.workOrder.objects.filter(Status=4, Location = emp.Location).count()
        if s4 > 0:
            OrderStatus.append('Pending Revised WO')
            OrderStatusValues.append(s4)
            status.append({'status':'Pending Revised WO', 'total': s4})
        s5 = woModels.workOrder.objects.filter(Status=5, Location = emp.Location).count()
        if s5 > 0:
            OrderStatus.append('Invoiced')
            OrderStatusValues.append(s5)
            status.append({'status':'Invoiced', 'total': s5})
    
    context["emp"] = emp
    context["per"] = per
    context["totalOrders"] = totalOrders
    context["payroll"] = totPayroll
    context["invoice"] = totInvoice
    context["perToPay"] = totPerc
    context["OrderStatus"] = OrderStatus
    context["OrderStatusValues"] = OrderStatusValues
    context["title"] ='Home Page'
    context["status"] = status
    context["year"] = datetime.now().year

    return render(
        request,
        'home.html',
        context        
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