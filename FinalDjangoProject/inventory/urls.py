from django.urls import path
from django.contrib.auth.views import LoginView
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'inventory'

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.custom_admin_login, name='custom_admin_login'),
    path('admin-generate-reports/', views.generate_reports, name='generate_reports'),
    path('admin-manage-users/', views.manage_users, name='manage_users'),
    path('register/', views.register_account, name='register_account'),
    path('approval-wait/', views.approval_wait, name='approval_wait'),
    path('login/', views.custom_login, name='custom_login'),
    path('user-dashboard/', views.user_dashboard_view, name='user_dashboard_view'),
    path('user-account-settings/', views.user_account_settings, name='user_account_settings'),
    path('admin-account-settings/', views.admin_account_settings, name='admin_account_settings'),
    path('user-item-list/', views.user_item_list, name='user_item_list'),
    path('admin-item-list/', views.admin_item_list, name='admin_item_list'),
    path('equipment-details/<int:equipment_id>/', views.equipment_details, name='equipment_details'),
    path('apply-reservation/<int:equipment_id>/', views.apply_reservation, name='apply_reservation'),
    path('admin-alerts/', views.admin_alerts, name='admin_alerts'),  # Path for the alerts page
    path('approve_booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject_booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('return-equipment/', views.return_equipment, name='return_equipment'),
    path('return-equipment/<int:item_id>/', views.process_return, name='process_return'),
    path('user-alerts/', views.user_alerts, name='user_alerts'),
    path('user-previous-bookings/', views.user_previous_bookings, name='user_previous_bookings'),
    path('admin-previous-bookings/', views.admin_previous_bookings, name='admin_previous_bookings'),
    path('admin-add-equipment/', views.add_equipment, name='add_equipment'),
    path('update-equipment/<int:equipment_id>/', views.update_equipment, name='update_equipment'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/inventory/admin-login/'), name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    # Add other URLs as needed...
]