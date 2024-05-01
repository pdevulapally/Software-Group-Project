from django.db import models
from django.contrib.auth.models import User
from .equipment import Equipment
# models.py

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    approval_status = models.BooleanField(default=False)  # Add this field
    returned = models.BooleanField(default=False)
    overdue_status = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.equipment.name} booked by {self.user.username}"