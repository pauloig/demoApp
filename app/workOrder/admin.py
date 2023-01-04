from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from workOrder.models import workOrder, workOrderDuplicate, Locations, Employee, item, itemPrice, payroll, payrollDetail, internalPO, period, Daily, DailyEmployee, DailyItem, employeeRecap, woStatusLog


admin.site.register(workOrder)
class  workOrderAdmin(ImportExportModelAdmin):
    list_display = ( 'id',
    'prismID',
    'workOrderId',
    'PO',
    'POAmount',
    'ConstType',
    'ConstCoordinator',
    'WorkOrderDate',
    'EstCompletion',
    'IssuedBy',
    'JobName',
    'JobAddress',
    'SiteContactName',
    'SitePhoneNumber',
    'Comments',
    'Status',
    'CloseDate',
    'WCSup',
    'UploadDate',
    'UserName' )

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
