from django.db import models

class Report(models.Model):
    report_type = models.CharField(max_length=200)
    current_inventory = models.TextField()
    usage_history = models.TextField()
    overdue_equipment = models.TextField()
    # Assuming this FK will be linked with Equipment
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)