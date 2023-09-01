from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login as login_process
from django.contrib.auth.decorators import login_required
from workOrder import models as woModels
from workOrder import views as woViews
from . import views


def calculate_payroll(locID):
    per = woModels.period.objects.filter(status__in=(1,2)).first()   
    
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
                    regular_time += validate_decimals(i.regular_hours)
                    over_time += validate_decimals(i.ot_hour)
                    double_time += validate_decimals(i.double_time)
                    total_time += validate_decimals(i.total_hours)
                    #if validate_decimals(i.EmployeeID.hourly_rate) != None:
                    rt += validate_decimals(i.rt_pay)
                    ot += validate_decimals(i.ot_pay)
                    dt += validate_decimals(i.dt_pay)

                if validate_decimals(i.bonus) != None:
                    bonus += validate_decimals(i.bonus)
                    
                if validate_decimals(i.on_call) != None:
                    on_call += validate_decimals(i.on_call)

                if validate_decimals(i.payout) != None:
                    payroll += validate_decimals(i.payout)

            
            dailyprod =  woModels.DailyItem.objects.filter(DailyID=dailyItem)
            total = 0
            
            ov = 0
            for j in dailyprod:                
                total += validate_decimals(j.total)
                if validate_decimals(j.price) != None:
                    invoice += (validate_decimals(j.quantity) * float(validate_decimals(j.price)) )
                if validate_decimals(j.emp_payout) != None:    
                    payroll2 += (validate_decimals(j.quantity) * float(validate_decimals(j.emp_payout)) )


            if validate_decimals(dailyItem.own_vehicle) != None:
                ov = validate_decimals(((validate_decimals(total) * validate_decimals(dailyItem.own_vehicle)) / 100))
                ownvehicle += validate_decimals(ov)
            prod += validate_decimals(total)

        if validate_decimals(invoice) > 0:                    
            perc = validate_decimals((validate_decimals(payroll) * 100) / validate_decimals(invoice))

        
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
    per = woModels.period.objects.filter(status__in=(1,2)).first()
    totPayroll=0 
    totInvoice=0 
    totPerc= 0
    OrderStatus = []
    OrderStatusValues = []
    status = []
    totalOrders = 0
    if emp:
        #Get total Orders by Rol
        if emp.is_superAdmin  or request.user.is_staff:
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
            if emp.Location!= None:
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

def validate_decimals(value):
    try:
        return round(float(str(value)), 2)
    except:
       return 0

def validate_print_decimals(value): 
    try:
        if round(float(value), 2) > 0:                
            return round(float(value), 2)
        else:
            return ''
    except:
       return ''    

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

            opType = "Log In"
            opDetail = "Login Successfull"

            woViews.logInAuditLog(request, opType, opDetail)

            return redirect('/home/')
        else:
            state = 2
            opType = "Log In"
            opDetail = "Login Failed, Username or password is incorrect - " + username + " -"

            woViews.logInAuditLog(request, opType, opDetail)

            message = "Username or password is incorrect"
    dic = {'state': state, 'message': message}
    return render(request, 'login.html', dic)