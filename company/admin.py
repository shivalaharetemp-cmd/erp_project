# company/admin.py
from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'gst_number', 'is_active']
    search_fields = ['name', 'gst_number']