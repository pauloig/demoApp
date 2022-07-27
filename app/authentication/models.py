from pyexpat import model
from django.db import models

class Sample(models.Model):
        attachment = models.FileField()
