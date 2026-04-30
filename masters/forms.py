# masters/forms.py
from django import forms
from .models import MasterType, Master


class MasterTypeForm(forms.ModelForm):
    class Meta:
        model = MasterType
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter type name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper().replace(' ', '_')
        return code


class MasterForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ['type', 'code', 'name', 'description', 'is_active']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
