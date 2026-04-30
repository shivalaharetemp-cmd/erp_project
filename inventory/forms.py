# inventory/forms.py
from django import forms
from .models import Item, StockTransaction


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['company', 'name', 'unit']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., PCS, KG, LTR'}),
        }


class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['company', 'item', 'quantity', 'type', 'reference', 'date']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'item': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reference'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
