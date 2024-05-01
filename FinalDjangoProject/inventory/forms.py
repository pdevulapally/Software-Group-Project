from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'serial_number', 'category', 'cpu', 'status', 'image_url']