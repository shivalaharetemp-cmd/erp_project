# accounts/admin.py
from django.contrib import admin
from .models import MasterGroup, Ledger, Voucher, VoucherEntry

class VoucherEntryInline(admin.TabularInline):
    model = VoucherEntry
    extra = 2

@admin.register(MasterGroup)
class MasterGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'type']
    list_filter = ['type']

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'group']
    list_filter = ['company', 'group']
    search_fields = ['name']

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['company', 'date', 'type', 'reference']
    list_filter = ['company', 'type', 'date']
    inlines = [VoucherEntryInline]