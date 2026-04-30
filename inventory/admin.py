# inventory/admin.py
from django.contrib import admin
from .models import Item, StockTransaction

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'unit']
    list_filter = ['company']

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['company', 'item', 'type', 'quantity', 'date']
    list_filter = ['company', 'type', 'date']