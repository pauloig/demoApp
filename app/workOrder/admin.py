from django.contrib import admin
from workOrder.models import *

@admin.register(workOrder)
class  workOrderAdmin(admin.ModelAdmin):
    list_display = ('prismID','workOrderId','PO')
    search_fields = ('prismID','workOrderId','PO')
    #list_filter = ('Location')

#admin.site.register(workOrder)
admin.site.register(workOrderDuplicate)
admin.site.register(Locations)
admin.site.register(Employee)
admin.site.register(item)
admin.site.register(itemPrice)
admin.site.register(payroll)
admin.site.register(payrollDetail)
admin.site.register(internalPO)
admin.site.register(period)
admin.site.register(Daily)
admin.site.register(DailyEmployee)
admin.site.register(DailyItem)
admin.site.register(employeeRecap)
admin.site.register(woStatusLog)
admin.site.register(vendor)
admin.site.register(subcontractor)
admin.site.register(externalProduction)
admin.site.register(externalProdItem)
admin.site.register(authorizedBilling)
admin.site.register(woEstimate)
admin.site.register(woInvoice)
admin.site.register(employeeLocation)
admin.site.register(billingAddress)

