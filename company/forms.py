# company/forms.py
from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'gst_number', 'address', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GST number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_gst_number(self):
        gst_number = self.cleaned_data.get('gst_number')
        if gst_number:
            gst_number = gst_number.upper().replace(' ', '')
            if len(gst_number) != 15:
                raise forms.ValidationError('GST number must be 15 characters')
        return gst_number
