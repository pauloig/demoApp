from turtle import home
from django.contrib import admin
from django.urls import path, include
from . import views
from timesheet import views

urlpatterns = [
     path('employee_list/',views.employee_list),   
     path('employee_submitted_list/',views.employee_submitted_list), 
     path('create/',views.create),
     path('update/<id>',views.update),
     path('create/',views.create),
     # ****** Supervisor **********************
     path('supervisor_list/',views.supervisor_list), 
     path('create_by_supervisor/',views.createBySupervisor),
     path('update_by_super/<id>',views.updateBySuper),
     path('update_status/<id>/<status>',views.update_status),
     path('reject_timesheet/<id>',views.reject_timesheet),
     path('approve_timesheet/<id>',views.approve_timesheet),
     # ****** Reports **********************
     path('report_list/',views.report_list), 
     path('get_report_list/<dateSelected>/<dateSelected2>/<status>/<location>/<employee>/<type>',views.get_report_list),
]