# workflow/admin.py
from django.contrib import admin
from .models import VehiclePlacement, Loading, Dispatch, Billing, WorkflowLog

@admin.register(VehiclePlacement)
class VehiclePlacementAdmin(admin.ModelAdmin):
    list_display = ['company', 'vehicle', 'placement_time', 'status']
    list_filter = ['company', 'status']

@admin.register(Loading)
class LoadingAdmin(admin.ModelAdmin):
    list_display = ['placement', 'start_time', 'end_time', 'status']
    list_filter = ['status']

@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = ['loading', 'dispatch_time', 'destination', 'status']
    list_filter = ['status']

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['dispatch', 'invoice_number', 'amount', 'status']
    list_filter = ['status']

@admin.register(WorkflowLog)
class WorkflowLogAdmin(admin.ModelAdmin):
    list_display = ['company', 'reference_id', 'stage', 'timestamp']
    list_filter = ['company', 'stage']