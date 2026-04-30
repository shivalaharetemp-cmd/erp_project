# workflow/forms.py
from django import forms
from .models import VehiclePlacement, Loading, Dispatch, Billing, WorkflowLog


class VehiclePlacementForm(forms.ModelForm):
    class Meta:
        model = VehiclePlacement
        fields = ['company', 'vehicle', 'placement_time', 'status']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'placement_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., PLACED'}),
        }


class LoadingForm(forms.ModelForm):
    class Meta:
        model = Loading
        fields = ['placement', 'start_time', 'end_time', 'supervisor', 'status']
        widgets = {
            'placement': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter supervisor name'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., LOADING, COMPLETED'}),
        }


class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = ['loading', 'dispatch_time', 'destination', 'transporter', 'status']
        widgets = {
            'loading': forms.Select(attrs={'class': 'form-select'}),
            'dispatch_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter destination'}),
            'transporter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter transporter name'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., DISPATCHED, DELIVERED'}),
        }


class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['dispatch', 'invoice_number', 'invoice_date', 'amount', 'status']
        widgets = {
            'dispatch': forms.Select(attrs={'class': 'form-select'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter invoice number'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., BILLING_PENDING, COMPLETED'}),
        }


class WorkflowLogForm(forms.ModelForm):
    class Meta:
        model = WorkflowLog
        fields = ['company', 'reference_id', 'stage']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'reference_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reference ID'}),
            'stage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stage name'}),
        }
