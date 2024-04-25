from django.db import models

class Equipment(models.Model):
    device_serial = models.CharField(max_length=200, primary_key=True)
    device_type = models.CharField(max_length=200)
    CPU = models.CharField(max_length=200)
    GPU = models.CharField(max_length=200)
    RAM = models.CharField(max_length=200)