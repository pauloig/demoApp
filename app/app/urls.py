"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('order_list/',views.listOrders),
    path('order_list_location/<str:userID>',views.order_list_location),
    path('order_list_sup/<str:userID>',views.order_list_sup),
    path('create_order/',views.create_order),
    path('order/<str:orderID>',views.order),
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
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('authentication.urls')),
     path('home/', include('authentication.urls')),
      path('',
         LoginView.as_view
         (
             template_name='authentication/login.html',
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