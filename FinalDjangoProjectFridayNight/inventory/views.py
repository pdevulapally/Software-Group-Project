from pyexpat.errors import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth.models import User

# Shows the inventory list with pagination
def show_inventory(request):
    equipments = [
        {'device_name': 'Laptop', 'device_type': 'Portable', 'serial_number': '12345', 'cpu': 'Intel i7', 'availability': 'Available'},
        {'device_name': 'Desktop', 'device_type': 'Stationary', 'serial_number': '67890', 'cpu': 'AMD Ryzen 7', 'availability': 'Unavailable'},
    ]

    for i in range(2, 40):
        equipments.append({
            'device_name': f'Product {i}',
            'device_type': f'Device Type {i}',
            'serial_number': f'Serial {i}',
            'cpu': f'CPU {i}',
            'availability': 'Available' if i % 2 == 0 else 'Unavailable'
        })

    paginator = Paginator(equipments, 10)  # Show 10 equipments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/admin-itemlist.html', {'page_obj': page_obj})

# Handles the admin dashboard view
@login_required(login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'inventory/admin-dashboard.html')

# Handles the admin login process
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'admin_login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'inventory/admin_login.html')

def generate_reports(request):
    return render(request, 'inventory/admin-generatereport.html')


from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Student, Admin, Staff
from django.db.models import Q

def manage_users(request):
    if request.method == 'POST':
        # Approve a student
        approve_id = request.POST.get('approve_id')
        if approve_id:
            try:
                student = Student.objects.get(user__id=approve_id)
                student.adminApprovalStatus = True
                student.save()
                messages.success(request, "Student has been approved.")
            except Student.DoesNotExist:
                messages.error(request, "No such student found.")
        
        # Delete a user
        delete_id = request.POST.get('delete_id')
        if delete_id:
            try:
                user = User.objects.get(id=delete_id)
                user.delete()
                messages.success(request, "User has been deleted.")
            except User.DoesNotExist:
                messages.error(request, "No such user found.")
        if 'approve_all' in request.POST:
            Student.objects.filter(adminApprovalStatus=False).update(adminApprovalStatus=True)
            messages.success(request, "All unapproved students have been approved.")

        if 'delete_all' in request.POST:
            User.objects.filter(
                Q(student_profile__adminApprovalStatus=False) | 
                Q(student_profile__isnull=True)
            ).delete()
            messages.success(request, "All unapproved users have been deleted.")
        
        # Redirect back to the same page to display messages
        return HttpResponseRedirect(reverse('manage_users'))
    

    users = User.objects.exclude(student_profile__adminApprovalStatus=True)
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    # Including additional data in the context
    context = {
        'users': users_page,
        'messages': messages.get_messages(request)
    }
    return render(request, 'inventory/admin-manageuser.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student, Staff  # Ensure your models are imported correctly

def register_account(request):
    if request.method == 'POST':
        # Basic user data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Create User
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Check role and create corresponding profile
        if role == 'student':
            grade = request.POST.get('grade')
            Student.objects.create(user=user, grade=grade)
        elif role == 'staff':
            job_role = request.POST.get('department')
            Staff.objects.create(user=user, job_role=job_role)

        messages.success(request, 'Registration successful!')
        return redirect('login')  # Redirect to a login page

    return render(request, 'inventory/approval.html')  # Adjust if you have a specific template path




