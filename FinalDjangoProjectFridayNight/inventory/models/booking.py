from django.db import models
from django.contrib.auth.models import User
from .equipment import Equipment

class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    approval_status = models.BooleanField()
    overdue_status = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)