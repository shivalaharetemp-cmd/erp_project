# masters/admin.py
from django.contrib import admin
from .models import MasterType, Master

class MasterInline(admin.TabularInline):
    model = Master
    extra = 1

@admin.register(MasterType)
class MasterTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    inlines = [MasterInline]

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['type', 'code', 'name', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['name', 'code']