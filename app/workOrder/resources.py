from pyexpat import model
from import_export import resources
from .models import workOrder, workOrderDuplicate

class workOrderResource(resources.ModelResource):
    class meta:
        model = workOrder
        exclude = ('id')


class workOrderDuplicateesource(resources.ModelResource):
    class meta:
        model = workOrderDuplicate
        exclude = ('id')