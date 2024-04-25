# inventory/models/users.py
from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return f"Admin: {self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    grade = models.CharField(max_length=10)  # Update the length according to your requirement

    def __str__(self):
        return f"Student: {self.user.username}"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    job_role = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):
        return f"Staff: {self.user.username}, Department: {self.department}"