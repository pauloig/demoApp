from datetime import datetime
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from authentication import forms, views
from authentication import views as viewHome
from workOrder import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/',views.simple_upload),
    path('upload_payroll/',views.upload_payroll),
    path('order_list/',views.listOrders),
    path('order_list_location/<str:userID>',views.order_list_location),
    path('order_list_sup/',views.order_list_sup),
    path('create_order/',views.create_order),
    path('order/<str:orderID>',views.order),
    path('order_supervisor/<str:orderID>',views.order_supervisor),
    path('truncateData/',views.truncateData),
    path('updateDupOrder/<str:pID>/<str:dupID>',views.updateDupOrder),
    path('insertDupOrder/<str:dupID>',views.insertDupOrder),
    path('deleteDupOrder/<str:pID>',views.deleteDupOrder),
    path('duplicate_order_list/',views.duplicatelistOrders),
    path('checkOrder/<str:pID>',views.checkOrder),
    path('location/',views.create_location),
    path('location_list/',views.location_list),
    path('update_location/<id>',views.update_location),
    path('employee_list/',views.employee_list),
    path('create_employee/',views.create_employee),
    path('update_employee/<id>',views.update_employee),
    path('link_order_list/<id>',views.linkOrderList),
    path('link_order/<id>/<manualid>',views.linkOrder),
    path('updateLinkOrder/<id>/<manualid>',views.updateLinkOrder),
    path('item_list/',views.item_list),
    path('create_item/',views.create_item),
    path('update_item/<id>',views.update_item),
    path('item_price/<id>',views.item_price),
    path('create_item_price/<id>',views.create_item_price),
    path('update_item_price/<id>',views.update_item_price),
    path('po_list/<id>',views.po_list),
    path('update_po/<id>',views.update_po),
    path('create_po/<id>',views.create_po),
    path('estimate_preview/<id>',views.estimate_preview),
    path('invoice_preview/<id>',views.invoice_preview),
    path('estimate/<id>',views.estimate),
    path('invoice/<id>',views.invoice),
    path('upload_item/',views.upload_item),
    path('upload_item_price/',views.upload_item_price),
    path('upload_employees/',views.upload_employee),
    path('period_list/',views.period_list),
    path('location_period_list/<id>',views.location_period_list),
    path('create_period/',views.create_period),
    path('orders_payroll/<dailyID>/<LocID>',views.orders_payroll, name="orders_payroll"),   
    path('payroll/<perID>/<dID>/<crewID>/<LocID>',views.payroll),
    path('update_order_daily/<woID>/<dailyID>/<LocID>',views.update_order_daily),
    path('create_daily/<pID>/<dID>/<LocID>',views.create_daily),
    path('update_daily/<daily>',views.update_daily),
    path('create_daily_emp/<id>/<LocID>',views.create_daily_emp),
    path('update_daily_emp/<id>/<LocID>',views.update_daily_emp),
    path('delete_daily_emp/<id>/<LocID>',views.delete_daily_emp),
    path('create_daily_item/<id>/<LocID>',views.create_daily_item),
    path('update_daily_item/<id>/<LocID>',views.update_daily_item),
    path('delete_daily_item/<id>/<LocID>',views.delete_daily_item),
    path('upload_daily/<id>/<LocID>',views.upload_daily),
    path('recap/<perID>',views.recap),
    path('send_recap/<perID>',views.send_recap),
    path('send_recap_emp/<perID>/<empID>',views.send_recap_emp),
    path('get_summary/<perID>',views.get_summary),
    path('update_sup_daily/<id>/<woid>',views.update_sup_daily),
    path('delete_daily/<id>/<LocID>',views.delete_daily),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('authentication.urls')),
    path('home/', include('authentication.urls')),
    
    path('',
         LoginView.as_view
         (
             template_name='login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context={
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
         path('login/',viewHome.login),
    ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )