from django.db import models

class Inventory(models.Model):
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=200)
    quantity = models.IntegerField()
    location = models.CharField(max_length=200)
    on_site_only = models.BooleanField()
    status = models.CharField(max_length=200)
    comments = models.TextField(blank=True, null=True)
    can_be_borrowed = models.BooleanField()