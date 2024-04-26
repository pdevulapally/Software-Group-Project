from django.db import models
from .booking import Booking

class Alert(models.Model):
    alert_message = models.TextField()
    alert_date_time = models.DateTimeField()
    acknowledge_status = models.BooleanField()
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
