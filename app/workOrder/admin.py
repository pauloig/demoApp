from django.contrib import admin
from workOrder.models import *

@admin.register(workOrder)
class  workOrderAdmin(admin.ModelAdmin):
    list_display = ('id','prismID','workOrderId','PO','Status')
    search_fields = ('id','prismID','workOrderId','PO','Status')
    list_filter = ('Status',)


class  authorizedBillingAdmin(admin.ModelAdmin):
    list_display = ('id','woID','itemID')
    search_fields = ('id','woID__prismID','woID__workOrderId','woID__PO')

class  internalPOAdmin(admin.ModelAdmin):
    list_display = ('id','poNumber')
    search_fields = ('id','poNumber')


class  internalPOAdmin(admin.ModelAdmin):
    list_display = ('id','poNumber')
    search_fields = ('id','poNumber')

class  DailyAdmin(admin.ModelAdmin):
    list_display = ('id','woID', 'crew', 'Location','Period','day')
    search_fields = ('id','woID')


admin.site.register(workOrderDuplicate)
admin.site.register(Locations)
admin.site.register(Employee)
admin.site.register(item)
admin.site.register(itemPrice)
admin.site.register(payroll)
admin.site.register(payrollDetail)
admin.site.register(internalPO,internalPOAdmin)
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
admin.site.register(authorizedBilling, authorizedBillingAdmin)
admin.site.register(woEstimate)
admin.site.register(woInvoice)
admin.site.register(employeeLocation)
admin.site.register(billingAddress)

