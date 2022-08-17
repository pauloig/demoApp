from pyexpat import model
from import_export import resources
from .models import workOrder

class workOrderResource(resources.ModelResource):
    class meta:
        model = workOrder