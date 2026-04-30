# accounts/forms.py
from django import forms
from .models import MasterGroup, Ledger, Voucher, VoucherEntry
from company.models import Company


class MasterGroupForm(forms.ModelForm):
    class Meta:
        model = MasterGroup
        fields = ['name', 'parent', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter group name'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }


class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = ['company', 'name', 'group']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ledger name'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
        }


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ['company', 'date', 'type', 'reference']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reference'}),
        }


class VoucherEntryForm(forms.ModelForm):
    class Meta:
        model = VoucherEntry
        fields = ['ledger', 'debit', 'credit']
        widgets = {
            'ledger': forms.Select(attrs={'class': 'form-select'}),
            'debit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'credit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }


VoucherEntryFormSet = forms.inlineformset_factory(
    Voucher, VoucherEntry, form=VoucherEntryForm,
    extra=2, can_delete=True, min_num=2, validate_min=True
)
