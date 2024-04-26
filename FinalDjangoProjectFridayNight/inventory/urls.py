from django.urls import path
from . import views

urlpatterns = [
    path('admin-item-list/', views.show_inventory, name='admin_item_list'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-generate-reports/', views.generate_reports, name='generate_reports'),
    path('admin-manage-users/', views.manage_users, name='manage_users'),
    path('register/', views.register_account, name='register_account'),
    # Add other URLs as needed...
]