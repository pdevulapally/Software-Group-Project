from datetime import timedelta
from pyexpat.errors import messages
from venv import logger
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def generate_reports(request):
    return render(request, 'inventory/admin-generatereport.html')


from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Student, Staff
from django.db.models import Q

def manage_users(request):


    if request.method == 'POST':
        approve_id = request.POST.get('approve_id')
        if approve_id:
            # Handle both students and staff approval
            user = User.objects.get(id=approve_id)
            if hasattr(user, 'student_profile'):
                user.student_profile.adminApprovalStatus = True
                user.student_profile.save()
            if hasattr(user, 'staff_profile'):
                user.staff_profile.adminApprovalStatus = True
                user.staff_profile.save()
            messages.success(request, "User has been approved.")

        delete_id = request.POST.get('delete_id')
        if delete_id:
            user = get_object_or_404(User, id=delete_id)
            # Ensure the user is unapproved before deleting
            if hasattr(user, 'student_profile') and not user.student_profile.adminApprovalStatus:
                user.delete()
                messages.success(request, "Unapproved student has been deleted.")
            elif hasattr(user, 'staff_profile') and not user.staff_profile.adminApprovalStatus:
                user.delete()
                messages.success(request, "Unapproved staff has been deleted.")
            else:
                messages.error(request, "Only unapproved users can be deleted.")

        if 'approve_all' in request.POST:
            Student.objects.filter(adminApprovalStatus=False).update(adminApprovalStatus=True)
            Staff.objects.filter(adminApprovalStatus=False).update(adminApprovalStatus=True)
            messages.success(request, "All unapproved users have been approved.")

        if 'delete_all' in request.POST:
            User.objects.filter(
                Q(student_profile__adminApprovalStatus=False) | 
                Q(staff_profile__adminApprovalStatus=False)
            ).delete()
            messages.success(request, "All unapproved users have been deleted.")

        return redirect('inventory:manage_users')

    # Fetch only users who are waiting for approval
    users_waiting_approval = User.objects.filter(
        Q(student_profile__adminApprovalStatus=False) |
        Q(staff_profile__adminApprovalStatus=False)
    )
    paginator = Paginator(users_waiting_approval, 10)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    return render(request, 'inventory/admin-manageuser.html', {'users': users_page})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Staff  # Ensure your models are imported correctly
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

def register_account(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Check if the email (used as username) already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'inventory/register.html')  # Return to the registration form

        # Validate password
        try:
            validate_password(password, user=None)
        except DjangoValidationError as e:
            messages.error(request, f"Password validation failed: {', '.join(e)}")
            return render(request, 'inventory/register.html')

        # Create User
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()

            # Check role and create corresponding profile
            if role == 'student':
                grade = request.POST.get('grade')  # Ensure you have a grade input in your form
                Student.objects.create(user=user, grade=grade, adminApprovalStatus=False)
            elif role == 'staff':
                job_role = request.POST.get('job_role')  # Ensure you have a job_role input in your form
                department = request.POST.get('department')  # Ensure you have a department input in your form
                if not job_role or not department:
                    messages.error(request, "All fields must be filled out for staff.")
                    user.delete()  # Clean up the partially created user
                    return render(request, 'inventory/register.html')
                Staff.objects.create(user=user, job_role=job_role, department=department, adminApprovalStatus=False)

            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('inventory:approval_wait')  # Redirect to the waiting for approval page
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'inventory/register.html')

    return render(request, 'inventory/register.html')




def approval_wait(request):
    # This view simply renders the waiting for approval page.
    return render(request, 'inventory/approval.html')


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)  # Or the name of the URL where you want to redirect the user
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'inventory/UsersLogin.html', {'form': form})


def user_dashboard_view(request):
    return render(request, 'inventory/user-dashboard.html')

@login_required
def user_account_settings(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        if 'password' in request.POST and request.POST['password']:
            user.set_password(request.POST['password'])
        if hasattr(user, 'student_profile'):
            user.student_profile.grade = request.POST.get('grade', user.student_profile.grade)
            user.student_profile.save()
        elif hasattr(user, 'staff_profile'):
            user.staff_profile.department = request.POST.get('department', user.staff_profile.department)
            user.staff_profile.save()
        user.save()
        login(request, user)  # Re-login the user after password change
        messages.success(request, 'Profile updated successfully!')
        return redirect('inventory:user_account_settings')
    return render(request, 'inventory/user-account-settings.html', {'user': request.user})

@login_required
def admin_account_settings(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        if 'password' in request.POST and request.POST['password']:
            user.set_password(request.POST['password'])
        if hasattr(user, 'student_profile'):
            user.student_profile.grade = request.POST.get('grade', user.student_profile.grade)
            user.student_profile.save()
        elif hasattr(user, 'staff_profile'):
            user.staff_profile.department = request.POST.get('department', user.staff_profile.department)
            user.staff_profile.save()
        user.save()
        login(request, user)  # Re-login the user after password change
        messages.success(request, 'Profile updated successfully!')
        return redirect('inventory:account_settings')
    return render(request, 'inventory/admin-account-settings.html', {'user': request.user})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Equipment, Booking

@login_required
def user_item_list(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('product[]')
        try:
            for item_serial in selected_items:
                equipment = Equipment.objects.get(device_serial=item_serial)
                Booking.objects.create(
                    user=request.user,
                    equipment=equipment,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=7),
                    approval_status=False
                )
            messages.success(request, "Your reservation has been submitted for approval.")
        except Equipment.DoesNotExist:
            messages.error(request, "One or more selected items could not be found.")
        return redirect('inventory/user-item-list')  # Redirect to a URL that is confirmed to exist
    else:
        equipment_list = Equipment.objects.all()
        paginator = Paginator(equipment_list, 10)  # Show 10 equipments per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventory/user-itemlist.html', {'page_obj': page_obj})
    

from django.db.models import Q
@login_required
def admin_item_list(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('product[]')
        try:
            for item_serial in selected_items:
                equipment = Equipment.objects.get(device_serial=item_serial)
                Booking.objects.create(
                    user=request.user,
                    equipment=equipment,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=7),
                    approval_status=False
                )
            messages.success(request, "Your reservation has been submitted for approval.")
        except Equipment.DoesNotExist:
            messages.error(request, "One or more selected items could not be found.")
        return redirect('inventory/admin-itemlist')  # Redirect to a URL that is confirmed to exist
    else:
        equipment_list = Equipment.objects.all()
        search_query = request.GET.get('search', '')  # Provide a default value if search query is None
        search_query = search_query.strip(", ")  # Strip any commas and spaces from the search query
        print("Search Query:", search_query)  # Debugging print statement

        equipment_list = Equipment.objects.all()
        if search_query:
            equipment_list = equipment_list.filter(name__icontains=search_query)
        paginator = Paginator(equipment_list, 10)  # Show 10 equipments per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventory/admin-itemlist.html', {'page_obj': page_obj})



from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Equipment, Booking

@login_required
def equipment_details(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    # Fetch the reservation where approval_status is True (meaning it's an active reservation)
    reservation = Booking.objects.filter(equipment=equipment, approval_status=True).first()

    if request.method == 'POST' and 'cancel_reservation' in request.POST:
        if reservation:
            # Update the equipment availability
            equipment.status = 'Available'
            equipment.save()
            # Cancel the reservation
            reservation.delete()  # Or mark as cancelled if you want to keep a record
            messages.success(request, "Reservation cancelled successfully.")
            return redirect('inventory:user_item_list')  # Redirect to a relevant page

    return render(request, 'inventory/equipment_details.html', {
        'equipment': equipment,
        'reservation': reservation
    })


@login_required
def apply_reservation(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)

    if request.method == 'POST':
        try:
            # Check if equipment is already reserved
            if Booking.objects.filter(equipment=equipment, approval_status=True).exists():
                messages.error(request, f"The equipment with serial {equipment.device_serial} is already reserved.")
            else:
                # Create reservation if equipment is available
                Booking.objects.create(
                    user=request.user,
                    equipment=equipment,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=7),
                    approval_status=False
                )
                messages.success(request, "Your reservation has been submitted for approval.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('inventory:equipment_details', equipment_id=equipment_id)
    
    return render(request, 'inventory/equipment_details.html', {'equipment': equipment})

def cancel_reservation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    equipment = booking.equipment
    if booking.approval_status:
        equipment.status = 'Available'
        equipment.save()
        booking.delete()  # Assuming you want to remove the booking altogether
        messages.success(request, "Reservation cancelled and equipment is now available.")
        return redirect('inventory:user_item_list')
    else:
        messages.error(request, "No active reservation to cancel.")
        return redirect('inventory:equipment_details', equipment_id=equipment.id)


# views.py

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def admin_alerts(request):
    pending_reservations = Booking.objects.filter(approval_status=False)
    return render(request, 'inventory/admin-alerts.html', {'pending_reservations': pending_reservations})

# views.py
from django.shortcuts import redirect
from django.contrib import messages
from .models import Booking

def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    equipment = booking.equipment
    equipment.status = 'Reserved'
    equipment.save()
    booking.approval_status = True
    booking.save()
    messages.success(request, "Reservation approved successfully!")
    return redirect('inventory:admin_alerts')

def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    equipment = booking.equipment
    equipment.status= 'Available'
    equipment.save()
    booking.delete()  # Or mark as rejected
    messages.success(request, "Booking rejected and equipment is now available.")
    return redirect('inventory:admin_alerts')


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

def custom_admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('inventory:admin_dashboard')
            else:
                messages.error(request, "Access denied: You are not an admin.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'inventory/admin-login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'inventory/admin-dashboard.html')
    else:
        return redirect('inventory:custom_admin_login')
    

@login_required
def return_equipment(request):
    # Fetch all bookings that have been approved but not returned.
    user_bookings = Booking.objects.filter(user=request.user, approval_status=True, returned=False)
    
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.returned = True
        booking.equipment.status = 'Available'  # Assuming you update the equipment status as well
        booking.equipment.save()
        booking.save()
        messages.success(request, "Equipment returned successfully.")
        return redirect('inventory/ReturnEquipment.html')  # Redirect to a confirmation page or back to the equipment list
    
    return render(request, 'inventory/ReturnEquipment.html', {'reserved_items': user_bookings})


@login_required
def process_return(request, item_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=item_id, user=request.user, approval_status=True)
        booking.equipment.availability = 'Available'
        booking.equipment.save()
        booking.returned = True
        booking.save()
        # Redirect to a confirmation page or back to the equipment list
        return redirect('inventory:return_equipment')
    

@login_required
def user_alerts(request):
    if request.method == 'POST' and 'dismiss' in request.POST:
        booking_id = request.POST.get('booking_id')
        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.is_dismissed = True
        booking.save()
        return redirect('inventory:user_alerts')

    approved_reservations = Booking.objects.filter(
        user=request.user, 
        approval_status=True, 
        is_dismissed=False
    )
    return render(request, 'inventory/user-alerts.html', {'approved_reservations': approved_reservations})


@login_required
def user_previous_bookings(request):
    bookings = Booking.objects.filter(user=request.user, returned=True).order_by('-end_date')
    return render(request, 'inventory/user-previous_bookings.html', {'bookings': bookings})

@login_required
def admin_previous_bookings(request):
    bookings = Booking.objects.filter(returned=True).order_by('-end_date')
    return render(request, 'inventory/admin-previous-bookings.html', {'bookings': bookings})

from .forms import EquipmentForm
from .models import Equipment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)  # Include request.FILES if handling files
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment added successfully!')
            return redirect('inventor/:admin_item_list.html')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentForm()
    return render(request, 'inventory/add_equipment.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipment
from .forms import EquipmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def update_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipment updated successfully!")
            return redirect('inventory:admin_item_list')
        else:
            messages.error(request, "Error updating equipment.")
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'inventory/update_equipment.html', {'form': form, 'equipment': equipment})


from django.shortcuts import render

def forgot_password(request):
    return render(request, 'inventory/forgot_password.html')
