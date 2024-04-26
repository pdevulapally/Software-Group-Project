# inventory/admin.py
from django.contrib import admin
from .models.users import Admin, Student, Staff
from .models.equipment import Equipment
from .models.inventory import Inventory
from .models.booking import Booking
from .models.report import Report
from .models.alert import Alert
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Custom method to display related user fields in the admin
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['get_username']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'  # Sets the column name

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'grade']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'  # Sets the column name

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'job_role', 'department']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'  # Sets the column name

# Register other models.
admin.site.register(Equipment)
admin.site.register(Inventory)
admin.site.register(Booking)
admin.site.register(Report)
admin.site.register(Alert)

# Optionally extend and register the built-in User model with custom admin
class UserAdmin(BaseUserAdmin):
    # Add the list_display settings, search_fields, etc., if you have custom fields in User model
    pass

# Re-register User model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
