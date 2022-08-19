from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from workOrder.models import workOrder, workOrderDuplicate

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