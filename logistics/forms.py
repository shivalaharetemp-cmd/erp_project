# logistics/forms.py
from django import forms
from .models import Vehicle, Shipment
from masters.models import Master


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_type']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., MH12AB1234',
                'pattern': '[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}'
            }),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data.get('vehicle_number')
        if vehicle_number:
            vehicle_number = vehicle_number.upper().replace(' ', '')
        return vehicle_number


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'company', 'supply_type', 'sub_supply_type', 'document_type',
            'transportation_mode', 'consignment_status', 'vehicle',
            'transaction_type', 'date'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'supply_type': forms.Select(attrs={'class': 'form-select'}),
            'sub_supply_type': forms.Select(attrs={'class': 'form-select'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'transportation_mode': forms.Select(attrs={'class': 'form-select'}),
            'consignment_status': forms.Select(attrs={'class': 'form-select'}),
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
