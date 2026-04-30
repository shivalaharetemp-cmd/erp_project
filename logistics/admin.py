# logistics/admin.py
from django.contrib import admin
from .models import Vehicle, Shipment

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'vehicle_type']
    search_fields = ['vehicle_number']

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['company', 'vehicle', 'supply_type', 'date']
    list_filter = ['company', 'supply_type', 'date']