# reports/forms.py
from django import forms
from django.db.models import Q
from company.models import Company
from accounts.models import Ledger, Voucher
from inventory.models import Item
from logistics.models import Vehicle
from masters.models import Master


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class CompanyFilterForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class LedgerFilterForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ledger = forms.ModelChoiceField(
        queryset=Ledger.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class StockFilterForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class VoucherFilterForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    voucher_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Voucher.VOUCHER_TYPES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class VehicleFilterForm(forms.Form):
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
