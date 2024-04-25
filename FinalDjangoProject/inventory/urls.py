# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('admin-item-list/', views.show_inventory, name='admin_item_list'),
]